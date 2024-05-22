from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.db import Base


class Geo(Base):
    id: int = Column(BigInteger, primary_key=True)
    name: str = Column(String(256), nullable=False)

    channel = relationship(
        'Channel',
        back_populates='geo',
    )
