from loguru import logger

from src.db import get_session
from src.models.channel import Channel
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
async def add_channel(channel_id: int, name: str) -> int:
    if len(str(channel_id)) < 14:
        channel_id = int(str(channel_id).replace('-', '-100'))
    new_channel = Channel(id=channel_id, name=name)
    with get_session() as session:
        session.add(new_channel)
    return channel_id


@log_func
async def delete_channel(channel) -> bool:
    with get_session() as session:
        session.delete(channel)
    return True
