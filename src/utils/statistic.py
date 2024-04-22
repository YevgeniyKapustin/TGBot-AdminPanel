import json
from datetime import datetime, timedelta

from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest

from src import config
from src.services.channel import get_channels
from src.services.userbot import get_userbot


async def get_new_subscribers_statistic():
    userbot = await get_userbot()
    client = TelegramClient(userbot.phone, config.API_ID, config.API_HASH)

    one_day_ago = datetime.now() - timedelta(days=1)
    new_subscribers_statistic: str = f'{one_day_ago.strftime("%d.%m.%y")}\n\n'
    all_sum = 0
    async with client:
        for channel in await get_channels():
            tl_channel = await client.get_entity(channel.id)
            channel_info = await client(
                GetFullChannelRequest(channel=tl_channel)
            )

            if channel_info.full_chat.can_view_stats:
                broadcast_stats = await client.get_stats(tl_channel)
                data = json.loads(broadcast_stats.followers_graph.json.data)
                last_subscribers: list[int, int] = data.get('columns')[1][-2]
                all_sum += last_subscribers
                string: str = f'{channel.name} - {last_subscribers}\n'
                new_subscribers_statistic += string

    new_subscribers_statistic += f'\nИтого: {all_sum}'
    return new_subscribers_statistic
