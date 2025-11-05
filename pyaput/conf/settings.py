from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APUT_")

    project_name: str = "pyaput"
    debug: bool = False
    aptly_api_url: str = "https://aptly.home.arpa/api/"
    aptly_api_auth_user: str = "admin"
    aptly_api_auth_pwd: str = "admin"
