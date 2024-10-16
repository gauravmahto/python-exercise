from functools import lru_cache

from warlock_utils_package import timing_decorator


@timing_decorator
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(50))  # Much faster due to caching
