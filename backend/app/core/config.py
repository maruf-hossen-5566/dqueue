import os

from dotenv import load_dotenv
from pydantic.networks import IPvAnyAddress, IPvAnyAddressType
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS").split(",")
    # admin
    ADMIN_USER: str = os.getenv("ADMIN_USER")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    ADMIN_IP_ADDRESS: str = os.getenv("ADMIN_IP_ADDRESS")
    # auth
    AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY")
    AUTH_TOKEN_EXPIRY_MINUTES: int = os.getenv("AUTH_TOKEN_EXPIRY_MINUTES")
    # db
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    # redis
    REDIS_URL: str = os.getenv("REDIS_URL")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_QUEUE_NAME: str = os.getenv("REDIS_QUEUE_NAME")
    # mail
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    # imagekit
    IMAGEKIT_ID: str = os.getenv("IMAGEKIT_ID")
    IMAGEKIT_URL: str = os.getenv("IMAGEKIT_URL")
    IMAGEKIT_API_KEY: str = os.getenv("IMAGEKIT_API_KEY")
    IMAGEKIT_IMAGE_FOLDER: str = os.getenv("IMAGEKIT_IMAGE_FOLDER")
    IMAGEKIT_FILE_FOLDER: str = os.getenv("IMAGEKIT_FILE_FOLDER")
    MAX_FILE_SIZE: int = os.getenv("MAX_FILE_SIZE")
    # resend
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    RESEND_EMAIL: str = os.getenv("RESEND_EMAIL")
    RESEND_NAME: str = os.getenv("RESEND_NAME")

    class Config:
        env_file = ".env"


settings = Settings()
