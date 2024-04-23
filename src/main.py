from aiogram import Dispatcher
from loguru import logger

from bot import bot
from src.handlers import start, permission, statistic, channels, userbot
from src.utils.schedule import scheduler


async def main() -> None:
    logger.info('launch...')

    dp: Dispatcher = Dispatcher()
    dp.include_routers(
        start.router,
        permission.router,
        statistic.router,
        channels.router,
        userbot.router,
    )
    scheduler.start()
    await dp.start_polling(bot)
