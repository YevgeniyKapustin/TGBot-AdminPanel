from bot import bot


async def get_channel_id(link: str | int) -> int:
    if str(link)[0] != '@' and 't.me/' in str(link):
        link = f'@{link.split('t.me/')[1]}'
    elif str(link)[0] == '-' or str(link)[0] == '@':
        ...
    else:
        return -1
    chat = await bot.get_chat(link)
    return chat.id


async def get_channel_username(link: str | int) -> str | None:
    if str(link)[0] != '@' and 't.me/' in str(link):
        link = f'@{link.split('t.me/')[1]}'
    elif str(link)[0] == '-' or str(link)[0] == '@':
        ...
    else:
        return None
    chat = await bot.get_chat(link)
    return chat.username
