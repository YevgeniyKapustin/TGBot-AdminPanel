from datetime import datetime

from loguru import logger

from src.services.channel import get_channel
from src.services.channel_statistic import get_channels_statistic


async def get_new_subscribers_statistic(date: datetime.date):
    new_subscribers_statistic: str = f'{date.strftime("%d.%m.%y")}\n\n'
    bolivia = '**Боливия**\n\n'
    columbia = '**Колумбия**\n\n'
    peru = '**Перу**\n\n'
    ecuador = '**Эквадор**\n\n'
    other = '**Нераспределенные**\n\n'
    # вот это можно было бы сделать через бд, но мне кажется так будет проще
    bolivia_sum = 0
    columbia_sum = 0
    peru_sum = 0
    ecuador_sum = 0
    other_sum = 0
    all_sum = 0

    for channel_statistic in await get_channels_statistic(date):
        all_sum += channel_statistic.new_subscribers
        channel = await get_channel(channel_statistic.channel_id)
        subs = int(channel_statistic.new_subscribers * 1.2)
        # очень костыльная компенсация пропадающих ивентов на участников
        string = get_new_string(channel.name, subs)
        if channel.name[:2] == 'БЛ':
            bolivia_sum += subs
            bolivia += string
        elif channel.name[:1] == 'К':
            columbia_sum += subs
            columbia += string
        elif channel.name[:1] == 'П':
            peru_sum += subs
            peru += string
        elif channel.name[:1] == 'Э':
            ecuador_sum += subs
            ecuador += string
        else:
            other_sum += subs
            other += string
    bolivia += f'_______________\nИтого: {bolivia_sum}\n'
    columbia += f'_______________\nИтого: {columbia_sum}\n'
    peru += f'_______________\nИтого: {peru_sum}\n'
    ecuador += f'_______________\nИтого: {ecuador_sum}\n'
    other += f'_______________\nИтого: {other_sum}\n'
    new_subscribers_statistic += f'\n**ИТОГО ВСЕ ГЕО: {all_sum}**'

    logger.info(new_subscribers_statistic)
    return new_subscribers_statistic


def get_new_string(name: str, subscribers: int) -> str:
    return f'{name} - {subscribers}\n'
