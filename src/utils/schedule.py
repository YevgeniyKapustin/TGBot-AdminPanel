from datetime import datetime, date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot import bot
from src.services.user import get_users
from src.utils.statistic import get_new_subscribers_statistic

scheduler = AsyncIOScheduler()


async def send_stats():
    stat_date: datetime.date = date.today() - timedelta(days=1)
    new_subscribers_statistic = await get_new_subscribers_statistic(stat_date)
    for user in await get_users():
        if user.has_access:
            await bot.send_message(user.id, new_subscribers_statistic)


scheduler.add_job(send_stats, CronTrigger.from_crontab('00 7 * * *'))
