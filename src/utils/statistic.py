from datetime import datetime

from loguru import logger

from src.services.channel import get_channel
from src.services.channel_statistic import get_channels_statistic


async def get_new_subscribers_statistic(date: datetime.date):
    new_subscribers_statistic: str = f'{date.strftime("%d.%m.%y")}\n\n'
    bolivia = '<b>Боливия</b>\n\n'
    columbia = '<b>Колумбия</b>\n\n'
    peru = '<b>Перу</b>\n\n'
    ecuador = '<b>Эквадор</b>\n\n'
    other = '<b>Нераспределенные</b>\n\n'
    bolivia_sum = 0
    columbia_sum = 0
    peru_sum = 0
    ecuador_sum = 0
    other_sum = 0
    all_sum = 0

    for channel_statistic in await get_channels_statistic(date):
        channel = await get_channel(channel_statistic.channel_id)
        subs = int(channel_statistic.new_subscribers * 1.3)
        all_sum += subs
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

    new_subscribers_statistic += (
        f'{bolivia}_______________\nИтого: {bolivia_sum}\n'
        f'Диалогов: ~{bolivia_sum * 0.8}\n\n'
    )
    new_subscribers_statistic += (
        f'{columbia}_______________\nИтого: {columbia_sum}\n'
        f'Диалогов: ~{bolivia_sum * 0.8}\n\n'
    )
    new_subscribers_statistic += (
        f'{peru}_______________\nИтого: {peru_sum}\n'
        f'Диалогов: ~{bolivia_sum * 0.8}\n\n'
    )
    new_subscribers_statistic += (
        f'{ecuador}_______________\nИтого: {ecuador_sum}\n'
        f'Диалогов: ~{bolivia_sum * 0.8}\n\n'
    )
    other = other[:25] if len(other) == 27 else other
    new_subscribers_statistic += (
        f'{other}_______________\nИтого: {other_sum}\n'
        f'Диалогов: ~{bolivia_sum * 0.8}\n\n'
    )
    new_subscribers_statistic += f'<b>ИТОГО ВСЕ ГЕО: {all_sum}</b>'

    logger.info(new_subscribers_statistic)
    return new_subscribers_statistic


def get_new_string(name: str, subscribers: int) -> str:
    return f'{name} - {subscribers}\n'
