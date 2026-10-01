import random
import time

from utils import timer
from utils import log_call
from utils import retry
from utils import memoize
from utils import Timer
from utils import timer_context


def fib(n):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


@memoize
def fib_memoized(n):
    if n <= 1:
        return n

    return fib_memoized(n - 1) + fib_memoized(n - 2)


print("Fibonacci without memoization")
start = time.perf_counter()
result = fib(32)
end = time.perf_counter()

print(f"fib(32) = {result}")
print(f"Time: {end - start:.6f} seconds")


print("\nFibonacci with memoization")
start = time.perf_counter()
result = fib_memoized(32)
end = time.perf_counter()

print(f"fib_memoized(32) = {result}")
print(f"Time: {end - start:.6f} seconds")


print("\nTesting @timer")


@timer
def slow_function():
    time.sleep(1)
    return "Done"


print(slow_function())


print("\nTesting @log_call")


@log_call
def add(a, b):
    return a + b


print(add(10, 20))


print("\nTesting @retry")


@retry(times=3, delay=1)
def flaky():
    if random.random() < 0.7:
        raise RuntimeError("Random failure")

    return "Success!"


try:
    print(flaky())
except RuntimeError:
    print("Function failed after all retry attempts")


print("\nTesting stacked decorators")


@timer
@log_call
def multiply(a, b):
    return a * b


print(multiply(5, 6))

print(f"\nFunction name: {multiply.__name__}")


print("\nTesting class-based Timer")

with Timer():
    time.sleep(1)


print("\nTesting contextlib Timer")

with timer_context():
    time.sleep(1)