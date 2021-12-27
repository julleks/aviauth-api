from datetime import datetime as original_datetime
from datetime import timedelta, timezone

from app.core.config import settings

__all__ = ["utc", "datetime", "timedelta"]


utc = timezone.utc


class datetime(original_datetime):
    @classmethod
    def now(cls, tz=utc if settings.USE_TZ else None):
        return super().now(tz)
