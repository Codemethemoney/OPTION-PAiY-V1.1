from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OPTION_PAY_AGENTS"
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "https://yourdomain.com"]

    class Config:
        env_file = ".env"

settings = Settings()
