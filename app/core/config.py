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

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
