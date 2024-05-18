from sqlalchemy import Column, BigInteger, ForeignKey, Date, Integer
from sqlalchemy.orm import relationship

from src.db import Base


class ChannelStatistic(Base):
    id: int = Column(BigInteger, primary_key=True)
    date: bool = Column(Date, nullable=False, default=False)
    channel_id: str = Column(
        BigInteger, ForeignKey('channel.id'), nullable=False
    )
    new_subscribers: int = Column(Integer, nullable=False, default=False)

    channel = relationship('Channel', back_populates='statistics')
