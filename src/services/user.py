from src.db import get_async_session
from src.models.user import User
from src.utils.log import log_func


@log_func
async def give_access(user: User) -> bool:
    user.has_access = True
    with get_async_session() as session:
        session.add(user)
    return user.has_access


@log_func
async def take_away_access(user: User) -> bool:
    user.has_access = False
    with get_async_session() as session:
        session.add(user)
    return user.has_access


@log_func
async def get_user(user_id: int) -> User:
    with get_async_session() as session:
        return session.query(User).filter(User.id == user_id).first()


@log_func
async def get_users() -> list[User]:
    with get_async_session() as session:
        return session.query(User).all()