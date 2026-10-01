import time
import functools
import contextlib


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")

        return result

    return wrapper


def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        print(f"Arguments: args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        print(f"Returned: {result}")

        return result

    return wrapper


def retry(times=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    print(f"Attempt {attempt}/{times} failed: {e}")

                    if attempt == times:
                        raise

                    time.sleep(delay)

        return wrapper

    return decorator


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))

        if key in cache:
            print(f"Cache hit for {func.__name__}{args}")
            return cache[key]

        print(f"Calculating {func.__name__}{args}")

        result = func(*args, **kwargs)
        cache[key] = result

        return result

    return wrapper


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start

        print(f"Block took {self.elapsed:.6f} seconds")


@contextlib.contextmanager
def timer_context():
    start = time.perf_counter()

    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"Block took {end - start:.6f} seconds")