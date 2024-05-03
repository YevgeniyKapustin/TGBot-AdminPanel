from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated

from src.services.channel_statistic import update_new_subscribers

router = Router()


@router.chat_member()
async def handle_new_subscriber(event: ChatMemberUpdated):
    if (
            event.new_chat_member.status == ChatMemberStatus.CREATOR or
            event.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR or
            event.new_chat_member.status == ChatMemberStatus.MEMBER
    ):
        await update_new_subscribers(event.date.date(), event.chat.id)
