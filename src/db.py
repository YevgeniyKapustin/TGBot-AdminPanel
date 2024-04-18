from contextlib import contextmanager

from loguru import logger
from sqlalchemy import Column, Integer, create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import (
    as_declarative, declared_attr, Mapped, Session, sessionmaker
)
from sqlalchemy.pool import NullPool

from src.utils.dsn import get_dsn


@as_declarative()
class Base:
    __name__: str
    id: Mapped[int] = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


engine: Engine = create_engine(get_dsn(), poolclass=NullPool)


@contextmanager
def get_session():
    session: Session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as exception:
        logger.critical(exception)
        session.rollback()
        logger.debug('session rollback')
    finally:
        session.close()
