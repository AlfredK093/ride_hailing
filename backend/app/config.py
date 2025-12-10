from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Malawi Ride-Hailing"
    DATABASE_URL: str
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REDIS_HOST: str = "redis"

    class Config:
        env_file = ".env"

settings = Settings()
