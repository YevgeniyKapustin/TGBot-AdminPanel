from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated
from loguru import logger

from src.services.channel_statistic import update_new_subscribers, \
    get_channel_statistic

router = Router()


@router.chat_member()
def handle_new_subscriber(event: ChatMemberUpdated):
    if (
            event.old_chat_member.status == ChatMemberStatus.LEFT and
            event.new_chat_member.status == ChatMemberStatus.MEMBER
    ):
        old = 0
        new = 0
        stat = get_channel_statistic(event.date.date(), event.chat.id)
        if stat:
            old = stat.new_subscribers

        update_new_subscribers(event.date.date(), event.chat.id)

        stat = get_channel_statistic(event.date.date(), event.chat.id)
        if stat:
            new = stat.new_subscribers
        if old + 1 != new:
            logger.error(f'old: {old}; new: {new};')
