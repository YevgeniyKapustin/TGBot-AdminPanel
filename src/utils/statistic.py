from datetime import datetime

from loguru import logger

from src.constants import messages
from src.models.channel import Channel
from src.services.channel import get_channels_by_geo, get_channels_without_geo
from src.services.channel_statistic import get_channel_statistic, \
    add_channel_statistic
from src.services.geo import get_geos


async def get_new_subscribers_statistic(date: datetime.date):
    result_message: str = f'{date.strftime("%d.%m.%y")}\n\n'
    general_subscribers: int = 0

    for geo in await get_geos():
        channels: list[Channel] = await get_channels_by_geo(geo.id)
        geo_content, geo_subscribers = await _get_channels_data(channels, date)
        general_subscribers += geo_subscribers
        result_message += await _get_new_block(
            name=geo.name,
            content=geo_content,
            subscribers=geo_subscribers
        )

    channels: list[Channel] = await get_channels_without_geo()
    lost_content, lost_subscribers = await _get_channels_data(channels, date)
    result_message += await _get_new_block(
            name=messages.not_defined_geo_name,
            content=lost_content,
            subscribers=lost_subscribers
        )

    result_message += (
        f'<b>ИТОГО ВСЕ ГЕО: {general_subscribers}</b>\n'
        f'Диалогов: ~{await _get_dialogs(general_subscribers)}'
    )

    logger.info(result_message)
    return result_message


async def _get_new_string(name: str, subscribers: int) -> str:
    return f'{name} - {subscribers}\n'


async def _get_new_block(name: str, content: str, subscribers: int):
    return (
        f'<b>{name}</b>\n'
        f'\n'
        f'{content}'
        f'_______________\n'
        f'Итого: {subscribers}\n'
        f'Диалогов: ~{await _get_dialogs(subscribers)}\n\n'
    )


async def _get_channels_data(channels: list, date) -> tuple[str, int]:
    content: str = ''
    subscribers: int = 0

    for channel in channels:
        channel_statistic = get_channel_statistic(date, channel.id)
        if not channel_statistic:
            await add_channel_statistic(channel.id, date)
            channel_statistic = get_channel_statistic(date, channel.id)
        channel_subscribers = int(channel_statistic.new_subscribers * 1.35)
        subscribers += channel_subscribers
        content += await _get_new_string(channel.name, channel_subscribers)

    return content, subscribers


async def _get_dialogs(subscribers: int) -> int:
    return int(subscribers * 0.8)
