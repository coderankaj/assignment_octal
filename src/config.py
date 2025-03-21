import os

from pydantic import Field
from pydantic_settings import BaseSettings

from src.app.settings import AppSettings
from . import FASTAPI_ENVIRONMENT


class Settings(BaseSettings):
    # General settings
    fastapi_env: str = FASTAPI_ENVIRONMENT
    debug: bool = True if FASTAPI_ENVIRONMENT in ["dev", "local"] else False

    # app and credentials settings
    app: AppSettings = Field(default_factory=AppSettings)

    # Server settings
    server_host: str = "localhost"
    server_port: int = 8000

    # Database
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "fastapi_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_super_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


settings = Settings()
