from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TOKEN: str

    MARIADB_USER: str
    MARIADB_PASSWORD: str
    MARIADB_HOST: str
    MARIADB_PORT: int
    MARIADB_DATABASE: str

    class Config:
        env_file_encoding = 'utf-8'
