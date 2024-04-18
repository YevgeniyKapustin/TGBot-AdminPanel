from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants import emojis
from src.models.user import User
from src.services.user import get_users
from src.utils.log import log_func


@log_func
async def create_permission_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    users: list[User] = await get_users()
    for count, user in enumerate(users, start=1):

        if user.has_access:
            emoji: str = emojis.active
        else:
            emoji: str = emojis.non_active
        builder.row(InlineKeyboardButton(
            text=f'{emoji} {count}. {user.username}',
            callback_data=f'user_config_{user.id}')
        )
    return builder
