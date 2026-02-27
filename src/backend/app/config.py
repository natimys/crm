from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: str = "8000"

    allowed_origins: list[str] = ["http://localhost:3000"]

    database_url: str
    
    secret_key: str = "change-this"
    algorithm: str = "HS256"
    access_token_expire_min: int = 30

    s3_endpoint: str = "http://minio:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "med-docs"
    

    class Config:
        env_file = ".env"

settings = Settings()