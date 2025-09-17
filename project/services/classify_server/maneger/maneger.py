from GroupAnalysis.project.services.classify_server.objects.temp_dir import TempDir
from GroupAnalysis.project.services.classify_server.handlers.data_handler.data_handler import DataHandler


class Manager:

    def __init__(self, db_handler, consumer, text_classified, visual_classified, categories):
        self.db_handler = db_handler
        self.consumer = consumer
        self.text_classified = text_classified
        self.visual_classified = visual_classified
        self.categories = categories
        self.data_handler = None

    def _fuse_modalities(self, video_vec=None, text_vec=None, audio_vec=None) -> str:
        """
        מאחד וקטורים לקטגוריה מנצחת לפי משקולות:
        וידאו 0.40, טקסט 0.30, אודיו 0.30
        """
        def _reduce(x):
            return x.mean(dim=0) if hasattr(x, "dim") and x.dim() == 2 else x

        parts, weights = {}, {}
        if video_vec is not None:
            parts["video"] = _reduce(video_vec)
            weights["video"] = 0.40
        if text_vec is not None:
            parts["text"] = _reduce(text_vec)
            weights["text"] = 0.30
        if audio_vec is not None:
            parts["audio"] = _reduce(audio_vec)
            weights["audio"] = 0.30

        if not parts:
            return None

        sw = sum(weights.values()) or 1.0
        weights = {k: v / sw for k, v in weights.items() if k in parts}

        out = None
        for k, v in parts.items():
            out = (weights[k] * v) if out is None else out + (weights[k] * v)
        out = out / (out.sum() + 1e-9)

        top_idx = int(out.argmax().item())
        return self.categories[top_idx]

    def manage(self):
        for msg in self.consumer.consume():
            file_id = msg.value["file_id"]
            with TempDir() as dir_path:
                his_type, file_path, text = self.db_handler.write_file_from_gridfs(file_id, dir_path)
                self.data_handler = DataHandler(file_path, dir_path)
                if his_type == "video":
                    category = self.video_handler(file_path, text)
                elif his_type == "audio":
                    category = self.audio_handler(file_path, text)
                elif his_type == "text":
                    category = self.text_handler(file_path)
                elif his_type == "image":
                    category = self.image_handler(file_path, text)
                if category:
                    self.db_handler.update_metadata_by_id(file_id, "classification", category)

    def video_handler(self, file_path, text) -> str:
        gen_img = DataHandler.gen_load_image(self.data_handler.frames_by_length())
        frames_matrix_vector = self.visual_classified.classify_frames(gen_img)

        gen_aud = self.data_handler.audio_segments_to_wav_by_length()
        audios_matrix_vector = self.text_classified.audios_classified(gen_aud)

        text_vector = self.text_classified.text_classified(text) if text else None

        return self._fuse_modalities(
            video_vec=frames_matrix_vector,
            text_vec=text_vector,
            audio_vec=audios_matrix_vector
        )

    def audio_handler(self, file_path, text) -> str:
        gen_aud = self.data_handler.audio_segments_to_wav_by_length()
        audios_matrix_vector = self.text_classified.audios_classified(gen_aud)

        text_vector = self.text_classified.text_classified(text) if text else None

        return self._fuse_modalities(
            audio_vec=audios_matrix_vector,
            text_vec=text_vector
        )

    def text_handler(self, file_path) -> str:
        text = DataHandler.get_text_from_file(file_path)
        text_vector = self.text_classified.text_classified(text)
        return self._fuse_modalities(text_vec=text_vector)

    def image_handler(self, file_path, text) -> str:
        img = DataHandler.load_image(file_path)
        img_vector = self.visual_classified.classify_openclip(img)  # חשוב: להעביר Image, לא path

        text_vector = self.text_classified.text_classified(text) if text else None

        return self._fuse_modalities(
            video_vec=img_vector,
            text_vec=text_vector
        )
