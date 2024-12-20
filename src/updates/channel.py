from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated

from src.services.channel_statistic import update_new_subscribers

router = Router()


@router.chat_member()
def handle_new_subscriber(event: ChatMemberUpdated):
    if (
            event.old_chat_member.status == ChatMemberStatus.LEFT and
            event.new_chat_member.status == ChatMemberStatus.MEMBER
    ):
        update_new_subscribers(event.date.date(), event.chat.id)
