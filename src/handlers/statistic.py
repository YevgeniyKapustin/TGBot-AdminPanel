from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.constants import buttons, messages
from src.filters.permission import PermissionFilter
from src.utils.keybords import get_manage_statistic_builder
from src.utils.statistic import get_new_subscribers_statistic

router = Router()


@router.message(F.text == buttons.statistics, PermissionFilter())
async def manage_statistic_handler(message: Message):
    logger.info(buttons.statistics)
    answer: str = messages.manage_statistic
    builder: InlineKeyboardBuilder = await get_manage_statistic_builder()
    logger.info(answer)

    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(
    F.data == 'statistic_new_subscribers',
    PermissionFilter()
)
async def get_new_subscribers_statistics_handler(callback: CallbackQuery):
    logger.info(buttons.new_subscribers_statistics)

    answer: str = await get_new_subscribers_statistic()
    logger.info(answer)
    await callback.message.delete()
    await callback.message.answer(answer)

    await manage_statistic_handler(callback.message)
