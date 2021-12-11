from logging import Logger
from typing import Callable

from tenacity import RetryCallState, _utils


def before_log(logger: Logger) -> Callable[[RetryCallState], None]:
    """Before call strategy that logs to structlog the attempt."""

    def log_it(retry_state: RetryCallState) -> None:
        logger.info(
            "Starting call",
            to=_utils.get_callback_name(retry_state.fn),
            attempt=retry_state.attempt_number,
        )

    return log_it


def after_log(
    logger: Logger,
    sec_format: str = "%0.3f",
) -> Callable[[RetryCallState], None]:
    """After call strategy that logs to structlog the finished attempt."""

    def log_it(retry_state: RetryCallState) -> None:
        logger.warn(
            "Finished call",
            to=_utils.get_callback_name(retry_state.fn),
            after=sec_format % retry_state.seconds_since_start,
            attempt=retry_state.attempt_number,
        )

    return log_it