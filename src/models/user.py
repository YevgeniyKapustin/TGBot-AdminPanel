from sqlalchemy import Column, BigInteger, String, Boolean

from src.db import Base


class User(Base):

    id: int = Column(BigInteger, primary_key=True)
    username: str = Column(String(256), nullable=False)
    has_access: bool = Column(Boolean, nullable=False, default=False)
    is_admin: bool = Column(Boolean, nullable=False, default=False)
