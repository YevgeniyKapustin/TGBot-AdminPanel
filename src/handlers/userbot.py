from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger
from pyrogram import Client
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneNumberUnoccupied, PhoneCodeInvalid,
    PhoneCodeExpired
)
from pyrogram.types import SentCode

from src import config
from src.constants import buttons, messages
from src.filters.permission import PermissionFilter
from src.models.user import User
from src.services.user import get_user
from src.services.userbot import delete_userbot, add_userbot
from src.states.add_userbot import AddUserbotState
from src.utils.keybords import (
    get_manage_userbot_builder, get_only_back_builder
)

router = Router()


@router.message(F.text == buttons.userbot, PermissionFilter())
async def manage_userbot_handler(message: Message):
    logger.info(buttons.userbot)

    user: User = await get_user(message.from_user.id)
    if user and not user.is_admin:
        answer: str = messages.access_denied
        logger.info(answer)
        return await message.answer(answer)

    answer: str = messages.manage_userbot
    builder: InlineKeyboardBuilder = await get_manage_userbot_builder()
    logger.info(answer)

    return await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data == 'userbot_add', PermissionFilter())
async def userbot_add_handler(callback: CallbackQuery, state: FSMContext):
    builder: InlineKeyboardBuilder = await get_only_back_builder()

    await state.set_state(AddUserbotState.phone)
    await callback.message.delete()

    await callback.message.answer(
        messages.userbot_phone,
        reply_markup=builder.as_markup()
    )


@router.message(AddUserbotState.phone, PermissionFilter())
async def userbot_phone(message: Message, state: FSMContext):
    phone: str = message.text
    logger.info(phone)
    try:
        client: Client = Client(
            name='userbot',
            api_id=config.API_ID,
            api_hash=config.API_HASH
        )
        await client.connect()
        sent_code: SentCode = await client.send_code(phone)
        await state.update_data(phone=phone)
        await state.update_data(client=client)
        await state.update_data(sent_code=sent_code.phone_code_hash)
        await state.set_state(AddUserbotState.code)
        await message.answer(messages.userbot_code)
    except PhoneNumberInvalid:
        await message.answer(messages.bad_phone, parse_mode='Markdown')


@router.message(AddUserbotState.code, PermissionFilter())
async def userbot_code(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sent_code: str = state_data.get('sent_code')
    phone: str = state_data.get('phone')
    client: Client = state_data.get('client')
    code: str = message.text

    logger.info(sent_code)

    try:
        await client.sign_in(phone, sent_code, code)
        await add_userbot(phone)
        await message.answer(messages.success_auth)
        await state.clear()
        await manage_userbot_handler(message)
    except PhoneNumberUnoccupied:
        await message.answer(messages.user_not_found)
    except PhoneCodeInvalid:
        await message.answer(messages.invalid_code)
    except PhoneCodeExpired:
        sent_code: SentCode = await client.send_code(phone)
        await state.update_data(sent_code=sent_code.phone_code_hash)
        await state.set_state(AddUserbotState.code)
        await message.answer(messages.expired_code)


@router.callback_query(F.data == 'back_settings', PermissionFilter())
async def back_settings(callback: CallbackQuery, state: FSMContext):
    logger.info(buttons.back)
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Отменено')


@router.callback_query(F.data == 'userbot_delete', PermissionFilter())
async def userbot_delete_handler(callback: CallbackQuery):
    logger.info(buttons.delete)
    await delete_userbot()
    await callback.message.delete()
    await manage_userbot_handler(callback.message)
