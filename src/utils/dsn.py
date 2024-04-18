from pydantic import MariaDBDsn

from src import config


def get_dsn() -> str:
    return str(MariaDBDsn.build(
        scheme='mariadb+pymysql',
        username=config.MARIADB_USER,
        password=config.MARIADB_PASSWORD,
        host=config.MARIADB_HOST,
        port=config.MARIADB_PORT,
        path=config.MARIADB_DATABASE
    ))
