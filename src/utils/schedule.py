from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot import bot
from src.services.user import get_users
from src.utils.statistic import get_new_subscribers_statistic

scheduler = AsyncIOScheduler()


async def send_stats():
    for user in await get_users():
        if user.has_access:
            await bot.send_message(
                user.id,
                await get_new_subscribers_statistic()
            )


scheduler.add_job(send_stats, CronTrigger.from_crontab('00 9 * * *'))
