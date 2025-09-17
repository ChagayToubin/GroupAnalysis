import os
import asyncio
from telethon import TelegramClient, events
from collections import defaultdict

from project.services.pull_data.app.kafka_producer import SetKafkaProducer

class TelegramDownloader:
    def __init__(self, api_id, api_hash, storage_manager, session_name="downloader_session"):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.storage = storage_manager
        self.download_folder = "downloads"
        os.makedirs(self.download_folder, exist_ok=True)
        self.album_cache = defaultdict(list)
        self.kafka_producer = SetKafkaProducer()
        self.kafka_producer.producer_config()
        self.topic = "telegram_messages"

    async def download_group_messages(self, group_link: str, limit=1000):
        """מוריד הודעות קיימות מהקבוצה כולל אלבומים"""

        # ✅ לוודא שהלקוח מחובר
        if not self.client.is_connected():
            await self.client.connect()

        group = await self.client.get_entity(group_link)
        print(f"✅ Connected to group: {group.title}")

        async for message in self.client.iter_messages(group, limit=limit):
            album_id = getattr(message, "grouped_id", None)

            if album_id:
                self.album_cache[album_id].append(message)
                continue

            await self._process_single_message(message, group_link, message.text or "")

        # טיפול באלבומים
        for album_id, messages in self.album_cache.items():
            caption = ""
            for msg in messages:
                if msg.text:
                    caption = msg.text
                    break
            for msg in messages:
                await self._process_single_message(msg, group_link, caption)

        self.album_cache.clear()

    async def start_listening(self, group_link):
        """מתחיל להאזין להודעות חדשות בזמן אמת"""

        # ✅ לוודא שהלקוח מחובר
        if not self.client.is_connected():
            await self.client.connect()

        @self.client.on(events.NewMessage(chats=group_link))
        async def handler(event):
            message = event.message
            album_id = getattr(message, "grouped_id", None)
            text = message.text or ""

            if album_id:
                self.album_cache[album_id].append(message)
                if len(self.album_cache[album_id]) > 1:
                    caption = ""
                    for msg in self.album_cache[album_id]:
                        if msg.text:
                            caption = msg.text
                            break
                    for msg in self.album_cache[album_id]:
                        await self._process_single_message(msg, group_link, caption)
                    self.album_cache.pop(album_id, None)
            else:
                await self._process_single_message(message, group_link, text)

        print(f"📡 Listening to group: {group_link} (press Ctrl+C to stop)")
        await self.client.run_until_disconnected()

    async def _process_single_message(self, message, group_link, text):
        msg_id = message.id
        user = message.sender_id
        date = message.date
        album_id = getattr(message, "grouped_id", None)
        media_files = []

        # ✅ בדיקה מקדימה – האם יש בכלל משהו לשמור
        media_present = message.photo or message.document or (text and text.strip())
        if not media_present:
            print(f"⚠️ Message {msg_id} is empty, skipped MongoDB and Kafka")
            return

        def _publish_to_kafka(file_id, category):
            """פונקציה פנימית – שולחת ל-Kafka רק אם file_id תקין"""
            if not file_id:
                print(f"⚠️ Message {msg_id}: file_id is None, skipping Kafka publish")
                return
            self.kafka_producer.producer_publish(self.topic, {
                "message_id": msg_id,
                "group_link": group_link,
                "file_id": str(file_id),
                "category": category
            })
            self.kafka_producer.producer_flush()
            print(f"📤 Message {msg_id}: published to Kafka with file_id={file_id}, category={category}")


        # ---- תמונות ----
        if message.photo:
            tmp_path = os.path.join(self.download_folder, f"photo_{msg_id}.jpg")
            path = await message.download_media(file=tmp_path)

            if path and os.path.exists(path) and os.path.getsize(path) > 0:

                file_id = self.storage.save_file(path, {
                    "message_id": msg_id,
                    "group_link": group_link,
                    "category": "image",
                    "caption": text,
                    "user": user,
                    "date": date,
                    "album_id": album_id
                })
                print(f"🔹 After save_file: file_id = {file_id}, path exists? {os.path.exists(path)}")
                _publish_to_kafka(file_id, "image")
                os.remove(path)
                media_files.append({"category": "image", "file_id": str(file_id)})
            else:
                print(f"⚠️ Message {msg_id}: photo download failed or empty")


        # ---- וידאו/אודיו/מסמכים ----
        elif message.document:
            tmp_path = os.path.join(self.download_folder, f"doc_{msg_id}")
            path = await message.download_media(file=tmp_path)

            if path and os.path.exists(path) and os.path.getsize(path) > 0:

                mime_type = message.document.mime_type or ""
                if "video" in mime_type:
                    category = "video"
                elif "audio" in mime_type:
                    category = "audio"
                else:
                    category = "document"

                file_id = self.storage.save_file(path, {
                    "message_id": msg_id,
                    "group_link": group_link,
                    "category": category,
                    "caption": text,
                    "user": user,
                    "date": date,
                    "album_id": album_id
                })
                print(f"🔹 After save_file: file_id = {file_id}, path exists? {os.path.exists(path)}")
                _publish_to_kafka(file_id, category)
                os.remove(path)
                media_files.append({"category": category, "file_id": str(file_id)})
            else:
                print(f"⚠️ Message {msg_id}: document download failed or empty")


        # ---- טקסט בלבד ----
        if text and not media_files:
            tmp_path = os.path.join(self.download_folder, f"text_{msg_id}.txt")
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(text)

            if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:

                file_id = self.storage.save_file(tmp_path, {
                    "message_id": msg_id,
                    "group_link": group_link,
                    "category": "text",
                    "caption": text,
                    "user": user,
                    "date": date,
                    "album_id": album_id
                })
                print(f"🔹 After save_file: file_id = {file_id}, path exists? {os.path.exists(tmp_path)}")
                _publish_to_kafka(file_id, "text")
                os.remove(tmp_path)
                media_files.append({"category": "text", "file_id": str(file_id)})
            else:
                print(f"⚠️ Message {msg_id}: text file empty or not created")


        print(f"💾 Saved message {msg_id} with {len(media_files)} media files")
