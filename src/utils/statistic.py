from datetime import datetime

from loguru import logger

from src.services.channel import get_channel
from src.services.channel_statistic import get_channels_statistic


async def get_new_subscribers_statistic(date: datetime.date):
    new_subscribers_statistic: str = f'{date.strftime("%d.%m.%y")}\n\n'
    all_sum = 0
    for channel_statistic in await get_channels_statistic(date):
        all_sum += channel_statistic.new_subscribers
        channel = await get_channel(channel_statistic.channel_id)
        new_subscribers_statistic += get_new_string(
            channel.name,
            channel_statistic.new_subscribers
        )
    new_subscribers_statistic += f'\nИтого: {all_sum}'
    logger.info(new_subscribers_statistic)
    return new_subscribers_statistic


def get_new_string(name: str, subscribers: int) -> str:
    return f'{name} - {subscribers}\n'
