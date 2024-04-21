from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from loguru import logger

from src.constants import buttons, messages
from src.models.user import User
from src.services.user import get_user, add_user

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id: int = message.from_user.id
    name: str = message.from_user.full_name
    user: User | None = await get_user(user_id)
    keyboard: list = [
        KeyboardButton(text=buttons.statistics),
        KeyboardButton(text=buttons.channels),
    ]

    if user is None:
        await add_user(user_id, name)
        user: User = await get_user(user_id)

    if not user.has_access:
        return await message.answer(messages.access_denied_start)
    else:
        if user.is_admin:
            keyboard.append(KeyboardButton(text=buttons.users_permissions))
            keyboard.append(KeyboardButton(text=buttons.userbot))
        logger.debug(f'/start для {message.from_user.first_name}')
        return await message.answer(
            messages.welcome,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[keyboard],
                resize_keyboard=True
            )
        )
