import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Nexly"
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    AGENT_ID: str = os.getenv("AGENT_ID", "")

    MAP_HUMAN = {"D": "dias", "MS": "meses", "YS": "anos", "W": "semanas"}


settings = Settings()
