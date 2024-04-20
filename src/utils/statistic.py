from pyrogram import Client
from pyrogram.raw import functions

from src import config
from src.services.channel import get_channels


async def get_new_subscribers_statistic():
    client = Client(
        name='user_bot',
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        phone_number=config.PHONE_NUMBER
    )
    async with client as app:
        for channel in await get_channels():
            pyro_channel = await app.resolve_peer(channel.link)
            result = await app.invoke(
                functions.stats.GetBroadcastStats(
                    channel=pyro_channel
                )
            )
            print(result)
