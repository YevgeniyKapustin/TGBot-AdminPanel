from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.db import Base


class Channel(Base):
    id: int = Column(BigInteger, primary_key=True)
    name: str = Column(String(256), nullable=False)

    statistics = relationship(
        'ChannelStatistic',
        back_populates='channel',
        cascade="all, delete-orphan"
    )
