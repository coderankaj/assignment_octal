import os
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class ContactDetailSettings(BaseSettings):
    name: str = Field(default_factory=lambda: os.getenv('FA_CONTACT_NAME', 'Ankaj Gupta'))
    email: str = Field(default_factory=lambda: os.getenv('FA_CONTACT_EMAIL', 'ankajinterview@gmail.com'))
    url: Optional[str] = Field(default_factory=lambda: os.getenv('FA_CONTACT_URL'))

    class Config:
        env_prefix = "FA_CONTACT_"
        extra = "ignore"


class AppSettings(BaseModel):
    name: str = Field(default_factory=lambda: os.getenv('FA_APP_NAME', 'My App'))
    description: str = Field(default_factory=lambda: os.getenv('FA_APP_DESCRIPTION', 'My App'))
    version: str = Field(default_factory=lambda: os.getenv('FA_APP_VERSION', '0.0.1'))
    summary: str = Field(default_factory=lambda: os.getenv('FA_APP_SUMMARY'))
    terms_of_service_url: str = Field(default_factory=lambda: os.getenv('FA_APP_TERMS_OF_SERVICE_URL'))
    gzip_minimum_size: int = 10000

    contact: ContactDetailSettings = Field(default_factory=ContactDetailSettings)

    class Config:
        env_prefix = "FA_APP_"
        extra = "ignore"
