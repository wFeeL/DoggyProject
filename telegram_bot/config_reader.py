import os
import logging
from dotenv import load_dotenv

class Settings:
    def __init__(self, bot_token, admin_telegram_id):
        self.bot_token: str = bot_token
        self.admin_telegram_id: str = admin_telegram_id



bot_logger = logging.getLogger()

# For local building use load_dotenv() and .env file

load_dotenv()
# Settings for telegram bot and admin telegram id
config = Settings(bot_token=os.environ['BOT_TOKEN'], admin_telegram_id=os.environ['ADMIN_TELEGRAM_ID'])