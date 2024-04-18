from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from src.constants import buttons, messages

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons.generate_screenshot)]
        ],
        resize_keyboard=True
    )
    await message.answer(
        messages.welcome_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
