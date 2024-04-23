import json
from datetime import datetime, timedelta

from loguru import logger
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError
from telethon.tl.functions.channels import GetFullChannelRequest

from src import config
from src.constants import emojis
from src.models.userbot import Userbot
from src.services.channel import get_channels
from src.services.userbot import get_userbot


async def get_new_subscribers_statistic():
    userbot: Userbot = await get_userbot()
    client = TelegramClient(userbot.phone, config.API_ID, config.API_HASH)

    one_day_ago: datetime = datetime.now() - timedelta(days=1)
    new_subscribers_statistic: str = f'{one_day_ago.strftime("%d.%m.%y")}\n\n'
    all_sum = 0

    async with client:
        for channel in await get_channels():
            try:
                tl_channel = await client.get_entity(channel.id)
                channel_info = await client(GetFullChannelRequest(tl_channel))
                if channel_info.full_chat.can_view_stats:
                    broadcast_stats = await client.get_stats(tl_channel)
                    data = json.loads(broadcast_stats.followers_graph.json.data)
                    last_subscribers: int = data.get('columns')[1][-2]
                    all_sum += last_subscribers
                    new_string: str = f'{channel.name} - {last_subscribers}\n'
                else:
                    new_string = f'{channel.name} - {emojis.block}\n'
            except ChannelPrivateError as ex:
                logger.error(ex)
                new_string = f'{channel.name} - {emojis.block}\n'
            new_subscribers_statistic += new_string

    new_subscribers_statistic += f'\nИтого: {all_sum}'
    return new_subscribers_statistic
