import asyncio

from loguru import logger

from src.main import main

if __name__ == "__main__":
    logger.add('.log', retention='7 day')
    asyncio.run(main())
