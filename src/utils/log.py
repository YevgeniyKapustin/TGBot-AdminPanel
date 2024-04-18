from loguru import logger


def log_func(func):
    def wrapper(*args, **kwargs):
        logger.debug(
            f'Call func {func.__name__} with args: {args}, kwargs: {kwargs}'
        )
        result = func(*args, **kwargs)
        logger.debug(f'func {func.__name__} returned: {result}')
        return result
    return wrapper
