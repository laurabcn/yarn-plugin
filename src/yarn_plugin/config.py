from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://yarn:yarn@db:5432/yarn_plugin"

    model_config = {"env_file": ".env"}


settings = Settings()
