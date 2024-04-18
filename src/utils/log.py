from loguru import logger


def log_func(func):
    def wrapper(*args, **kwargs):
        logger.debug(
            f'Call func {func.__name__} with args: {args}, kwargs: {kwargs}'
        )
        return func(*args, **kwargs)
    return wrapper
