from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://yarn:yarn@db:5432/yarn_plugin"
    admin_secret: str = "change-me-in-production"
    jwt_secret: str = "change-me-in-production"
    jwt_expire_hours: int = 24
    base_url: str = "http://localhost:8000"

    model_config = {"env_file": ".env"}


settings = Settings()
