from aiogram import Bot, Dispatcher
from loguru import logger

from src import config


async def main() -> None:
    logger.info('launch...')
    bot: Bot = Bot(config.TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_routers()
    await dp.start_polling(bot)

