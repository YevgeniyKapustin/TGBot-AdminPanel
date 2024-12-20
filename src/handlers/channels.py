from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.constants import buttons, messages, emojis
from src.filters.permission import PermissionFilter
from src.models.channel import Channel
from src.models.user import User
from src.services.channel import (
    get_channel, add_channel, delete_channel, change_channel_geo,
    get_channel_geo_name
)
from src.services.channel_statistic import add_channel_statistic
from src.services.user import get_user
from src.states.channel import AddChannelState
from src.utils.channel import get_channel_id
from src.utils.geo import get_geo_from_date
from src.utils.keybords import (
    get_manage_channels_builder, get_manage_channel_builder,
    get_add_geo_builder, change_geo_builder
)

router = Router()


@router.message(F.text == buttons.channels, PermissionFilter())
async def manage_channels_handler(message: Message, state: FSMContext):
    logger.info(buttons.channels)

    user: User = await get_user(message.from_user.id)
    if user and not user.is_admin:
        answer: str = messages.access_denied
        logger.info(answer)
        return await message.answer(answer)

    await state.clear()
    answer: str = messages.manage_channels
    builder: InlineKeyboardBuilder = await get_manage_channels_builder()
    logger.info(answer)
    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data == 'manage_channels', PermissionFilter())
async def back_my_projects_handler(callback: CallbackQuery, state: FSMContext):
    logger.info(buttons.back)
    await callback.message.delete()
    await manage_channels_handler(callback.message, state)


@router.callback_query(
    F.data.startswith('channel_config:'),
    PermissionFilter()
)
async def manage_channel_handler(callback: CallbackQuery):
    channel_id: int = int(callback.data.split(':')[1])
    channel: Channel = await get_channel(channel_id)
    await callback.message.delete()

    answer: str = (
        f'{channel.name}({channel.id})\n'
        f'{emojis.pin} {await get_channel_geo_name(channel)}'
    )
    builder = await get_manage_channel_builder(channel.id)
    logger.info(answer)
    return await callback.message.answer(
        answer, reply_markup=builder.as_markup()
    )


@router.callback_query(
    F.data.startswith('channel_delete:'),
    PermissionFilter()
)
async def delete_channel_handler(callback: CallbackQuery, state: FSMContext):
    channel_id: int = int(callback.data.split(':')[1])
    channel: Channel = await get_channel(channel_id)
    await delete_channel(channel)
    await callback.message.delete()
    await manage_channels_handler(callback.message, state)


@router.callback_query(
    F.data.startswith('change_channel_geo:'),
    PermissionFilter()
)
async def set_geo_handler(callback: CallbackQuery):
    channel_id: int = int(callback.data.split(':')[1])

    await callback.message.delete()
    answer: str = messages.manage_geo
    builder: InlineKeyboardBuilder = await change_geo_builder(channel_id)
    logger.info(answer)

    return await callback.message.answer(
        answer,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith('change_geo:'), PermissionFilter())
async def final_add_channel(callback: CallbackQuery, state: FSMContext):
    geo_id: int = get_geo_from_date(callback.data.split(':')[1])
    channel_id: int = int(callback.data.split(':')[2])
    await change_channel_geo(channel_id, geo_id)

    await callback.message.delete()

    answer: str = messages.success_change_name
    logger.info(answer)
    await callback.message.answer(answer)
    await manage_channels_handler(callback.message, state)


@router.callback_query(F.data == 'channel_add', PermissionFilter())
async def set_link_for_channel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddChannelState.set_link)
    await callback.message.delete()
    answer: str = messages.add_channel_link
    logger.info(answer)
    await callback.message.answer(answer)


@router.message(AddChannelState.set_link, PermissionFilter())
async def set_name_for_channel(message: Message, state: FSMContext):
    channel_id: int = await get_channel_id(message.text)
    if await get_channel(channel_id):
        answer: str = messages.add_channel_duplicate_link
        logger.info(answer)
        return message.answer(answer)

    await state.update_data(channel_id=channel_id)
    await state.set_state(AddChannelState.set_name)

    answer: str = messages.add_channel_name
    logger.info(answer)
    await message.answer(answer)


@router.message(AddChannelState.set_name, PermissionFilter())
async def set_geo_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    answer: str = messages.add_channel_geo
    builder: InlineKeyboardBuilder = await get_add_geo_builder()
    logger.info(answer)

    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('set_geo:'), PermissionFilter())
async def final_add_channel(callback: CallbackQuery, state: FSMContext):
    state_data: dict = await state.get_data()

    channel_id: int = state_data.get('channel_id')
    name: str = state_data.get('name')
    geo_id: int = get_geo_from_date(callback.data.split(':')[1])

    if await get_channel(await get_channel_id(channel_id)):
        answer: str = messages.add_channel_duplicate_name
        logger.info(answer)
        return callback.message.answer(answer)

    if channel_id != -1:
        await add_channel(channel_id, name, geo_id)
        await add_channel_statistic(channel_id)
    else:
        await callback.message.answer(messages.add_channel_incorrect_link)

    await state.clear()
    await callback.message.delete()

    answer: str = messages.add_channel_finally
    logger.info(answer)
    await callback.message.answer(answer)
    await manage_channels_handler(callback.message, state)
