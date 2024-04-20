from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.constants import buttons, messages
from src.filters.permission import PermissionFilter
from src.models.channel import Channel
from src.services.channel import get_channel, add_channel, delete_channel
from src.state.add_channel import AddChannelState
from src.utils.channel import get_channel_id, get_channel_username
from src.utils.keybords import (
    get_manage_channels_builder, get_manage_channel_builder
)

router = Router()


@router.message(F.text == buttons.channels, PermissionFilter())
async def manage_channels(message: Message, state: FSMContext):
    logger.info(buttons.channels)

    await state.clear()
    answer: str = messages.manage_channels
    builder: InlineKeyboardBuilder = await get_manage_channels_builder()
    logger.info(answer)
    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data == 'manage_channels', PermissionFilter())
async def back_my_projects(callback: CallbackQuery, state: FSMContext):
    logger.info(buttons.back)
    await callback.message.delete()
    await manage_channels(callback.message, state)


@router.callback_query(
    F.data.startswith('channel_config:'),
    PermissionFilter()
)
async def manage_channel(callback: CallbackQuery):
    channel_id: int = int(callback.data.split(':')[1])
    channel: Channel = await get_channel(channel_id)
    await callback.message.delete()

    answer: str = f'{channel.name}({channel.id})'
    builder = await get_manage_channel_builder(channel.id)
    logger.info(answer)
    return await callback.message.answer(
        answer, reply_markup=builder.as_markup()
    )


@router.callback_query(
    F.data.startswith('channel_delete:'),
    PermissionFilter()
)
async def channel_delete(callback: CallbackQuery, state: FSMContext):
    channel_id: int = int(callback.data.split(':')[1])
    channel: Channel = await get_channel(channel_id)
    await delete_channel(channel)

    await manage_channels(callback.message, state)


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
    await state.set_state(AddChannelState.choosing_name)

    answer: str = messages.add_channel_name
    logger.info(answer)
    await message.answer(answer)


@router.message(AddChannelState.choosing_name, PermissionFilter())
async def final_add_channel(message: Message, state: FSMContext):
    state_data: dict = await state.get_data()

    channel_id: int = state_data.get('channel_id')
    name: str = message.text

    if await get_channel(await get_channel_id(channel_id)):
        answer: str = messages.add_channel_duplicate_name
        logger.info(answer)
        return message.answer(answer)

    username = await get_channel_username(channel_id)
    if channel_id != -1:
        await add_channel(channel_id, name, username)
    else:
        await message.answer(messages.add_channel_incorrect_link)

    await state.clear()

    answer: str = messages.add_channel_finally.format(name)
    logger.info(answer)
    await message.answer(answer)
    await manage_channels(message, state)
