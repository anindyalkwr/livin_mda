import os
from dotenv import load_dotenv, find_dotenv, get_key
from pydantic_settings import BaseSettings

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI E-commerce"
    API_V1_STR: str = "/api/v1"

    # Database - Reading directly from the .env file path
    DB_USER: str = get_key(dotenv_path, "POSTGRES_USER")
    DB_PASSWORD: str = get_key(dotenv_path, "POSTGRES_PASSWORD")
    DB_SERVER: str = get_key(dotenv_path, "DB_SERVER")
    DB_PORT: str = get_key(dotenv_path, "DB_PORT")
    DB_NAME: str = get_key(dotenv_path, "POSTGRES_DB")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

    # Security
    SECRET_KEY: str = get_key(dotenv_path, "SECRET_KEY")
    ALGORITHM: str = get_key(dotenv_path, "ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_key(dotenv_path, "ACCESS_TOKEN_EXPIRE_MINUTES"))

    class Config:
        case_sensitive = True

settings = Settings()