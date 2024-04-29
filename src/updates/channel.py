from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated
from loguru import logger

from src.services.channel_statistic import update_new_subscribers

router = Router()


@router.chat_member()
async def handle_new_subscriber(event: ChatMemberUpdated):
    logger.debug(event.new_chat_member.status)
    if event.new_chat_member.status == ChatMemberStatus.CREATOR:
        await update_new_subscribers(event.date.date(), event.chat.id)
