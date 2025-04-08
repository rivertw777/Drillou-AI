from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "MAINTAIN AI API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    OPENAI_API_KEY: str

    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://127.0.0.1:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
