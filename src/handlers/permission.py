from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.constants import buttons, messages
from src.filters.permission import PermissionFilter
from src.models.user import User
from src.services.user import get_user, take_away_access, give_access
from src.utils.keybords import create_permission_builder

router = Router()


@router.message(F.text == buttons.users_permissions, PermissionFilter())
async def manage_permissions(message: Message):
    logger.info(buttons.users_permissions)

    user: User = await get_user(message.from_user.id)
    if user and not user.is_admin:
        answer: str = messages.access_denied
        logger.info(answer)
        return await message.answer(answer)

    answer: str = messages.select_access_user
    builder: InlineKeyboardBuilder = await create_permission_builder()
    logger.info(answer)
    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('user_config_'), PermissionFilter())
async def change_access_state_for_user(callback: CallbackQuery):
    user_id: int = int(callback.data.split('_')[2])
    user: User = await get_user(user_id)
    logger.info(f'Изменить доступ юзера {user.username}')
    if user.id == callback.from_user.id:
        await callback.message.answer(messages.select_access_self)
        await callback.message.delete()
        return await manage_permissions(callback.message)

    if user.has_access:
        await take_away_access(user)
    else:
        await give_access(user)

    await callback.message.delete()
    return await manage_permissions(callback.message)
