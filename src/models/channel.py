from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base


class Channel(Base):
    id: int = Column(BigInteger, primary_key=True)
    name: str = Column(String(256), nullable=False)
    geo_id: int = Column(BigInteger, ForeignKey('geo.id'), nullable=True)

    geo = relationship('Geo', back_populates='channel')
    statistics = relationship(
        'ChannelStatistic',
        back_populates='channel',
        cascade="all, delete-orphan"
    )
