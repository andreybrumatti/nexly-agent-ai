import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Nexly"
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    AGENT_ID: str = os.getenv("AGENT_ID", "")

    MAP_HUMAN = {"D": "dias", "MS": "meses", "YS": "anos", "W": "semanas"}

    TIMEZONE_STR: str = "America/Sao_Paulo"

    @property
    def TZ_INFO(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE_STR)


settings = Settings()
