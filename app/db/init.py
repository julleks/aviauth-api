from sqlalchemy import select
from structlog import get_logger
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.packages.tenacity import after_log, before_log

from .session import engine

logger = get_logger()


@retry(
    stop=stop_after_attempt(settings.MAX_DB_CONNECTION_RETRIES),
    wait=wait_fixed(settings.DB_CONNECTION_RETRY_WAIT_SECONDS),
    before=before_log(logger),
    after=after_log(logger),
)
async def init_db() -> None:
    logger.info("Initializing DB")

    try:
        async with engine.begin() as conn:
            await conn.execute(select(1))

    except Exception as e:
        logger.error(e)
        raise e

    logger.info("DB finished initializing")
