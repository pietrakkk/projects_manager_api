from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: PostgresDsn = Field(validation_alias="DB_URL")
    db_echo: bool = Field(validation_alias="DB_ECHO", default=False)
    log_level: str = Field(validation_alias="LOG_LEVEL", default="INFO")


settings = Settings()
