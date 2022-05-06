"""Module for helpful functions not related to API."""
import functools
import logging
import time
from typing import Any, Callable

import coloredlogs
import numpy as np

from config import LOGGING_LEVEL

logger = logging.getLogger(__name__)
coloredlogs.install(
    level="DEBUG",
    logger=logger,
    fmt="%(asctime)s %(name)s [%(process)d] %(levelname)s %(message)s",
)


def time_and_log(
    add_func_args: bool = False,
    level: str = LOGGING_LEVEL,
) -> Callable:
    """Decorate any function to time and log start and end."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:

            # add city name if possible
            try:
                logging_method = getattr(logger, level.lower())

                # process started
                logging_method(
                    {
                        "process": func.__name__,
                        "message": "Started.",
                        "args": kwargs if add_func_args else "removed",
                    }
                )
                start_time = time.time()
                result = func(*args, **kwargs)

                # process finished
                logging_method(
                    {
                        "process": func.__name__,
                        "message": "Success.",
                        "elapsed_seconds": np.round(time.time() - start_time, 4),
                    }
                )
                return result

            # process error
            except Exception as e:
                logger.exception({"process": func.__name__, "error_msg": str(e)})
                raise e

        return wrapper

    return decorator
