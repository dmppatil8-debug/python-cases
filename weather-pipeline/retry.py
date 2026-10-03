import time
from functools import wraps


def retry(max_attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as error:
                    last_error = error

                    if attempt < max_attempts:
                        time.sleep(delay)

            raise last_error

        return wrapper

    return decorator