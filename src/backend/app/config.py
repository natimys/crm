from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/database"
    secret_key: str = "change-this"
    algorithm: str = "HS256"
    access_token_expire_min: int = 30

    class Config:
        env_file = ".env"

settings = Settings()