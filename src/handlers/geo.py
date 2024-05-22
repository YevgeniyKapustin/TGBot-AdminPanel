from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.constants import buttons, messages
from src.filters.permission import PermissionFilter
from src.models.geo import Geo
from src.models.user import User
from src.services.geo import delete_geo, get_geo, add_geo
from src.services.user import get_user
from src.states.add_geo import AddGeoState
from src.utils.keybords import get_manage_geo_builder


router = Router()


@router.message(F.text == buttons.geo, PermissionFilter())
async def manage_geo_handler(message: Message, state: FSMContext):
    logger.info(buttons.geo)

    user: User = await get_user(message.from_user.id)
    if user and not user.is_admin:
        answer: str = messages.access_denied
        logger.info(answer)
        return await message.answer(answer)

    await state.clear()
    answer: str = messages.manage_geo
    builder: InlineKeyboardBuilder = await get_manage_geo_builder()
    logger.info(answer)
    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('delete_geo:'), PermissionFilter())
async def delete_channel_handler(callback: CallbackQuery, state: FSMContext):
    geo_id: int = int(callback.data.split(':')[1])
    geo: Geo = await get_geo(geo_id)
    await delete_geo(geo)
    await callback.message.delete()
    await manage_geo_handler(callback.message, state)


@router.callback_query(F.data == 'new_geo', PermissionFilter())
async def manage_channel_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddGeoState.set_name)
    await callback.message.delete()
    answer: str = messages.add_geo_name
    logger.info(answer)
    await callback.message.answer(answer)


@router.message(AddGeoState.set_name, PermissionFilter())
async def set_geo_handler(message: Message, state: FSMContext):
    await add_geo(message.text)

    await state.clear()

    answer: str = messages.add_geo_finally
    logger.info(answer)
    await message.answer(answer)
    await manage_geo_handler(message, state)
