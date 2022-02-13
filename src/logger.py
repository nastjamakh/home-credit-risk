"""Module for helpful functions not related to API."""
from typing import Callable, Any, Tuple
import logging
import coloredlogs
import functools
import time
import numpy as np

from config import (
    LOGGING_LEVEL,
)


class CustomAdapter(logging.LoggerAdapter):
    """Custom logging adapter to add city name when available."""

    def process(self, msg: Any, kwargs: Any) -> Tuple[str, Any]:
        """Add city name to logs."""
        my_context = kwargs.pop("city_name", self.extra["city_name"])
        return "[%s] %s" % (my_context, msg), kwargs


logger = logging.getLogger(__name__)
coloredlogs.install(
    level=LOGGING_LEVEL,
    logger=logger,
    fmt="%(asctime)s %(name)s [%(process)d] %(levelname)s %(message)s",
)
city_logger = CustomAdapter(logger, {"city_name": "NO_CITY"})


def time_and_log(
    add_func_args: bool = False,
    level: str = LOGGING_LEVEL,
    has_city_attr: bool = False,
) -> Callable:
    """Decorate any function to time and log start and end."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:

            # add city name if possible
            city_name = kwargs.get("city_name", "NO_CITY")
            if has_city_attr:
                city_name = args[0].city.name
            try:
                logging_method = getattr(city_logger, level.lower())
                logging_method = functools.partial(logging_method, city_name=city_name)

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
                logging_method = functools.partial(
                    city_logger.exception, city_name=city_name
                )
                city_logger.exception({"process": func.__name__, "error_msg": str(e)})
                raise e

        return wrapper

    return decorator
