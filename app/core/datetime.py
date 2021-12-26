from datetime import datetime, timezone

from app.core.config import settings

utc = timezone.utc


def now():
    return datetime.now(tz=utc if settings.USE_TZ else None)
