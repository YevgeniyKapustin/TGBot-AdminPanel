from sqlalchemy import Column, BigInteger, String

from src.db import Base


class Channel(Base):
    id: int = Column(BigInteger, primary_key=True)
    name: str = Column(String(256), nullable=False)
    link: str = Column(String(256), nullable=False)
