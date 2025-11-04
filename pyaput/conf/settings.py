from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "pyaput"
    debug: bool = False
