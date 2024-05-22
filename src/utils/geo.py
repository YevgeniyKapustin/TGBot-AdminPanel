def get_geo_from_date(data: str) -> int:
    return int(data) if data.isdigit() else -1
