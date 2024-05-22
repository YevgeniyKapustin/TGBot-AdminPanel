from src.db import get_session
from src.models.geo import Geo
from src.utils.log import log_func


@log_func
async def get_geo(geo_id: int) -> Geo | None:
    with get_session() as session:
        geo = (
            session.query(Geo).
            filter(Geo.id == geo_id).
            first()
        )
        return geo


@log_func
async def get_geos() -> list[Geo]:
    with get_session() as session:
        return session.query(Geo).order_by(Geo.name).all()


@log_func
async def add_geo(name: str) -> str:
    new_geo = Geo(name=name)
    with get_session() as session:
        session.add(new_geo)
    return name


@log_func
async def delete_geo(geo: Geo) -> bool:
    with get_session() as session:
        session.delete(geo)
    return True
