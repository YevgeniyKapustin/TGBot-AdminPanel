from aiogram import Dispatcher
from loguru import logger

from bot import bot
from src.handlers import start, permission, statistic, channels, userbot


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
    await dp.start_polling(bot)
