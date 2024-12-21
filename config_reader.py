from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    admins_ids: SecretStr

    mysql_host: SecretStr
    mysql_user: SecretStr
    mysql_password: SecretStr
    mysql_db_name: SecretStr

    webhook: SecretStr
    webhook_host: SecretStr
    webhook_port: SecretStr
    webhook_base_url: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
