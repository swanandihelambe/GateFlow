from app.config import ROUTES


def resolve_route(path: str) -> str | None:
    return ROUTES.get(path)