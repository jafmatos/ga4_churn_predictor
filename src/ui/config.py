from pydantic_settings import SettingsConfigDict
from pydantic import Field
from pathlib import Path
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env.streamlit"


class Settings(BaseSettings):
    API_BASE_URL: str = Field(..., description="URL base da API")
    API_SECRET_KEY: str = Field(..., description="Chave de API da aplicação")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

API_BASE_URL=settings.API_BASE_URL
API_SECRET_KEY=settings.API_SECRET_KEY