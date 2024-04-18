from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from loguru import logger

from src.constants.messages import access_denied
from src.models.user import User
from src.services.user import get_user


class PermissionFilter(Filter):

    async def __call__(self, message: Message | CallbackQuery) -> bool:
        logger.debug(f'Проверка наличия доступа у {message.from_user.id}')
        user: User = await get_user(message.from_user.id)
        if user:
            if user.has_access:
                logger.debug(f'Успешная проверка доступа для {message.from_user.id}')
                return True
        else:
            logger.debug(f'Юзер {message.from_user.id} не имеет доступ к боту')
            await message.answer(access_denied.accessDenied)
            return False
