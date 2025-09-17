
from project.services.pull_data.app.telegram_manager import TelegramManager

manager = TelegramManager()
group_link = "https://t.me/TheBigBadShadow"

manager.run_monitor(group_link)

