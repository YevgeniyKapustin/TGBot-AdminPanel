from datetime import datetime, date, timedelta

from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from bot import bot
from src.services.user import get_users
from src.utils.statistic import get_new_subscribers_statistic

scheduler = AsyncIOScheduler()


async def send_staqts():
    stat_date: datetime.date = date.today() - timedelta(days=1)
    new_subscribers_statistic = await get_new_subscribers_statistic(stat_date)
    for user in await get_users():
        if user.has_access:
            try:
                await bot.send_message(
                    chat_id=user.id,
                    text=new_subscribers_statistic,
                    parse_mode=ParseMode.HTML
                )
            except TelegramForbiddenError as ex:
                logger.debug(ex)

scheduler.add_job(send_stats, CronTrigger.from_crontab('30 05 * * *'))
