from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants import emojis, buttons
from src.models.channel import Channel
from src.models.geo import Geo
from src.models.user import User
from src.services.channel import get_channels
from src.services.geo import get_geos
from src.services.user import get_users
from src.services.userbot import get_userbot
from src.utils.log import log_func


@log_func
async def get_permission_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    users: list[User] = await get_users()
    for count, user in enumerate(users, start=1):

        emoji: str = emojis.active if user.has_access else emojis.non_active
        status: str = emojis.star if user.is_admin else ''

        builder.row(InlineKeyboardButton(
            text=f'{emoji}{status} {count}. {user.username}',
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
    builder.row(InlineKeyboardButton(
        text=buttons.new_subscribers_statistics_today,
        callback_data=f'statistic_new_subscribers_today'),
    )
    return builder


@log_func
async def get_manage_channels_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    channels: list[Channel] = get_channels()
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
        text=f'{buttons.change_geo}',
        callback_data=f'change_channel_geo:{channel_id}')
    )
    builder.row(InlineKeyboardButton(
        text=f'{buttons.back}',
        callback_data=f'manage_channels')
    )
    return builder


@log_func
async def get_manage_userbot_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if await get_userbot():
        builder.row(InlineKeyboardButton(
            text=f'{buttons.delete}',
            callback_data=f'userbot_delete')
        )
    else:
        builder.row(InlineKeyboardButton(
            text=f'{buttons.add}',
            callback_data=f'userbot_add')
        )
    return builder


@log_func
async def get_only_back_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text='Отменить',
        callback_data='back')
    )
    return builder


@log_func
async def get_add_geo_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    geos: list[Geo] = await get_geos()
    for count, geo in enumerate(geos, start=1):
        builder.row(InlineKeyboardButton(
            text=f'{count}. {geo.name}',
            callback_data=f'set_geo:{geo.id}')
        )
    builder.row(InlineKeyboardButton(
        text=f'{buttons.no_geo}',
        callback_data=f'set_geo:-1')
    )
    return builder


@log_func
async def get_manage_geo_builder() -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text=buttons.add,
        callback_data=f'new_geo'),
    )
    geos = await get_geos()
    for count, geo in enumerate(geos, start=1):
        builder.row(InlineKeyboardButton(
            text=f'{count}. {buttons.delete_geo} {geo.name}',
            callback_data=f'delete_geo:{geo.id}'),
        )
    return builder


@log_func
async def change_geo_builder(channel_id) -> InlineKeyboardBuilder:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    geos: list[Geo] = await get_geos()
    for count, geo in enumerate(geos, start=1):
        builder.row(InlineKeyboardButton(
            text=f'{count}. {geo.name}',
            callback_data=f'change_geo:{geo.id}:{channel_id}')
        )
    builder.row(InlineKeyboardButton(
        text=f'{buttons.no_geo}',
        callback_data=f'change_geo:-1:{channel_id}')
    )
    return builder
