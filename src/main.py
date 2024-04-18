from aiogram import Bot, Dispatcher
from loguru import logger

from src import config
from src.handlers import permission


async def main() -> None:
    logger.info('launch...')
    bot: Bot = Bot(config.TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_routers(
        permission.router,
    )
    await dp.start_polling(bot)
