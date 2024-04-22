from bot import bot
from src.utils.log import log_func


@log_func
async def get_channel_id(link: str | int) -> int:
    link = str(link)
    if link[0] != '@' and 't.me/' in link:
        link = f'@{link.split('t.me/')[1]}'
    elif link[0] == '@':
        ...
    elif link[0] == '-':
        return int(link)
    else:
        return -1
    chat = await bot.get_chat(link)
    return chat.id


@log_func
async def get_channel_username(link: str | int) -> str | None:
    link = str(link)
    if link[0] != '@' and 't.me/' in link:
        link = f'@{link.split('t.me/')[1]}'
    elif link[0] == '@':
        ...
    elif link[0] == '-':
        return link
    else:
        return None
    chat = await bot.get_chat(link)
    return chat.username
