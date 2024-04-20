from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants import emojis, buttons
from src.models.channel import Channel
from src.models.user import User
from src.services.channel import get_channels
from src.services.user import get_users
from src.utils.log import log_func


@log_func
async def get_permission_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    users: list[User] = await get_users()
    for count, user in enumerate(users, start=1):

        if user.has_access:
            emoji: str = emojis.active
        else:
            emoji: str = emojis.non_active
        builder.row(InlineKeyboardButton(
            text=f'{emoji} {count}. {user.username}',
            callback_data=f'user_config:{user.id}')
        )
    return builder


@log_func
async def get_manage_statistic_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text=buttons.new_subscribers_statistics,
        callback_data=f'statistic_new_subscribers'),
    )
    return builder


@log_func
async def get_manage_channels_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    channels: list[Channel] = await get_channels()
    for channel in channels:
        builder.row(InlineKeyboardButton(
            text=channel.name,
            callback_data=f'channel_config:{channel.id}')
        )
    builder.row(InlineKeyboardButton(
        text=f'{buttons.add}',
        callback_data=f'channel_add')
    )
    return builder


@log_func
async def get_manage_channel_builder(channel_id: int) -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text=f'{buttons.delete}',
        callback_data=f'channel_delete:{channel_id}')
    )
    builder.row(InlineKeyboardButton(
        text=f'{buttons.back}',
        callback_data=f'manage_channels')
    )
    return builder
