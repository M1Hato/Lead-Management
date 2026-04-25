from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str

    JWT_SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

