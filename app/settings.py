from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    local_dev: str = Field(validation_alias='LOCAL_DEV', default=False)

    db_url: PostgresDsn = Field(validation_alias='DB_URL')
    db_echo: bool = Field(validation_alias='DB_ECHO', default=False)

    # aws_access_key_id: str = Field(validation_alias='AWS_ACCESS_KEY_ID')
    # aws_secret_access_key: str = Field(validation_alias='AWS_SECRET_ACCESS_KEY')
    # aws_bucket_name: str = Field(validation_alias='AWS_BUCKET_NAME')
    # aws_region_name: str = Field(validation_alias='AWS_REGION_NAME')
    # s3_obj_expiry_time: int = Field(validation_alias='S3_OBJ_EXPIRY_TIME', default=3600)


settings = Settings()