import os
import logging
import json
from dotenv import load_dotenv

class Settings:
    def __init__(self, bot_token, admin_telegram_ids):
        self.bot_token: str = bot_token
        self.admin_telegram_ids: list = admin_telegram_ids


def _json_list_env(name: str, default: list[int] | None = None) -> list[int]:
    """Парсит JSON-массив из env, например: [123, 456]."""

    raw = (os.getenv(name) or "").strip()
    if not raw:
        return list(default or [])
    try:
        value = json.loads(raw)
        if isinstance(value, list):
            out: list[int] = []
            for x in value:
                try:
                    out.append(int(x))
                except Exception:
                    continue
            return out
        # допускаем одиночное число
        try:
            return [int(value)]
        except Exception:
            return list(default or [])
    except Exception:
        return list(default or [])

bot_logger = logging.getLogger()

# For local building use load_dotenv() and .env file
img_path = f"{os.path.dirname(__file__)}/img"
load_dotenv()
# Settings for telegram bot and admin telegram id
config = Settings(bot_token=os.environ['BOT_TOKEN'], admin_telegram_ids=_json_list_env("ADMIN_TELEGRAM_ID", default=[]))