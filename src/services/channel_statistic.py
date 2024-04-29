import datetime

from sqlalchemy.sql.operators import and_

from src.db import get_session
from src.models.channel_statistic import ChannelStatistic
from src.services.channel import get_channels
from src.utils.log import log_func


@log_func
async def get_channels_statistic(
        date: datetime.date
) -> list[ChannelStatistic]:
    with get_session() as session:
        channels_statistic = (
            session.query(ChannelStatistic).
            filter(ChannelStatistic.date == date).
            all()
        )
        if not channels_statistic:
            await add_channels_statistic(date)
            channels_statistic = await get_channels_statistic(date)
        return channels_statistic


@log_func
async def get_channel_statistic(
        date: datetime.date, channel_id: int
) -> ChannelStatistic:
    with get_session() as session:
        channel_statistic = (
            session.query(ChannelStatistic).
            filter(
                and_(
                    ChannelStatistic.date == date,
                    ChannelStatistic.channel_id == channel_id
                )
            ).first()
        )
        return channel_statistic


@log_func
async def add_channels_statistic(date: datetime.date) -> bool:
    with get_session() as session:
        for channel in await get_channels():
            new_channel_statistic = ChannelStatistic(
                date=date,
                channel_id=channel.id,
                new_subscribers=0
            )
            session.add(new_channel_statistic)
        return True


@log_func
async def add_channel_statistic(channel_id: int) -> bool:
    with get_session() as session:
        new_channel_statistic = ChannelStatistic(
            date=datetime.date.today(),
            channel_id=channel_id,
            new_subscribers=0
        )
        session.add(new_channel_statistic)
        return True


@log_func
async def update_new_subscribers(date: datetime.date, channel_id: int) -> bool:
    with get_session() as session:
        statistic = await get_channel_statistic(date, channel_id)
        if not statistic:
            await add_channels_statistic(date)
            statistic = await get_channel_statistic(date, channel_id)
        statistic.new_subscribers += 1
        session.add(statistic)
        return True
