from typing import Callable

from structlog import BoundLogger
from tenacity import RetryCallState, _utils


def before_log(logger: BoundLogger) -> Callable[[RetryCallState], None]:
    """Before call strategy that logs to structlog the attempt."""

    def log_it(retry_state: RetryCallState) -> None:
        logger.info(
            "Starting a call",
            to=_utils.get_callback_name(retry_state.fn),
            attempt=retry_state.attempt_number,
        )

    return log_it


def after_log(
    logger: BoundLogger,
    sec_format: str = "%0.3f",
) -> Callable[[RetryCallState], None]:
    """After call strategy that logs to structlog the finished attempt."""

    def log_it(retry_state: RetryCallState) -> None:
        logger.warn(
            "Call finished",
            to=_utils.get_callback_name(retry_state.fn),
            after=sec_format % retry_state.seconds_since_start,
            attempt=retry_state.attempt_number,
        )

    return log_it
