from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TOKEN: str

    class Config:
        env_file_encoding = 'utf-8'
