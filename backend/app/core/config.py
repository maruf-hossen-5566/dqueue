import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS").split(",")
    ADMIN_USER: str = os.getenv("ADMIN_USER")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_QUEUE_NAME: str = os.getenv("REDIS_QUEUE_NAME")
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    IMAGEKIT_ID: str = os.getenv("IMAGEKIT_ID")
    IMAGEKIT_URL: str = os.getenv("IMAGEKIT_URL")
    IMAGEKIT_API_KEY: str = os.getenv("IMAGEKIT_API_KEY")
    IMAGEKIT_IMAGE_FOLDER: str = os.getenv("IMAGEKIT_IMAGE_FOLDER")
    IMAGEKIT_FILE_FOLDER: str = os.getenv("IMAGEKIT_FILE_FOLDER")
    MAX_FILE_SIZE: int = os.getenv("MAX_FILE_SIZE")

    class Config:
        env_file = ".env"


settings = Settings()
