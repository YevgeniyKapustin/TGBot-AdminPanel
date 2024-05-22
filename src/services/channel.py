from loguru import logger

from src.constants import messages
from src.db import get_session
from src.models.channel import Channel
from src.services.geo import get_geo
from src.utils.log import log_func


@log_func
async def get_channel(channel_id: int) -> Channel | None:
    with get_session() as session:
        channel = (
            session.query(Channel).
            filter(Channel.id == channel_id).
            first()
        )
        if channel:
            logger.info(f'Получен канал {channel.name}({channel.id})')
        else:
            logger.info(f'Канал {channel_id} не найден')
        return channel


@log_func
def get_channels() -> list[Channel]:
    with get_session() as session:
        return session.query(Channel).order_by(Channel.name).all()


@log_func
async def add_channel(channel_id: int, name: str, geo_id: int | None) -> int:
    geo_id = None if geo_id == -1 else geo_id
    if len(str(channel_id)) < 14:
        channel_id = int(str(channel_id).replace('-', '-100'))
    new_channel = Channel(id=channel_id, name=name, geo_id=geo_id)
    with get_session() as session:
        session.add(new_channel)
    return channel_id


@log_func
async def delete_channel(channel) -> bool:
    with get_session() as session:
        session.delete(channel)
    return True


@log_func
async def change_channel_geo(channel_id: int, geo_id: int) -> bool:
    geo_id = None if geo_id == -1 else geo_id
    channel: Channel = await get_channel(channel_id=channel_id)
    with get_session() as session:
        channel.geo_id = geo_id
        session.add(channel)
    return True


@log_func
async def get_channel_geo_name(channel: Channel) -> str:
    geo = await get_geo(channel.geo_id)
    return geo.name if geo else messages.not_defined_geo_name


@log_func
async def get_channels_by_geo(geo_id: int) -> list[Channel]:
    with get_session() as session:
        return (
            session.query(Channel).
            filter(Channel.geo_id == geo_id).
            order_by(Channel.name).
            all()
        )


@log_func
async def get_channels_without_geo() -> list[Channel]:
    with get_session() as session:
        return (
            session.query(Channel).
            filter(Channel.geo_id == None).
            order_by(Channel.name).
            all()
        )
