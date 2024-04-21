from src.db import get_session
from src.models.userbot import Userbot
from src.utils.log import log_func


@log_func
async def get_userbot() -> Userbot | None:
    with get_session() as session:
        return session.query(Userbot).first()


@log_func
async def delete_userbot() -> bool:
    with get_session() as session:
        session.delete(await get_userbot())
    return True


@log_func
async def add_userbot(phone: str) -> str:
    new_channel = Userbot(phone=phone)
    with get_session() as session:
        session.add(new_channel)
    return phone
