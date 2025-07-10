import os
from dotenv import load_dotenv
# Remove the PostgresDsn import
from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Any, Dict, Optional

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mock Livin MDA"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_SERVER: str
    DB_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None

    @model_validator(mode='before')
    def get_database_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(values.get("DATABASE_URL"), str):
            return values
        dsn = (
            f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@"
            f"{values.get('DB_SERVER')}:{values.get('DB_PORT')}/{values.get('POSTGRES_DB')}"
        )
        values["DATABASE_URL"] = dsn
        return values

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True

settings = Settings()