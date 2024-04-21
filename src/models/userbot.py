from sqlalchemy import Column, String

from src.db import Base


class Userbot(Base):
    phone: str = Column(String(20), primary_key=True)
