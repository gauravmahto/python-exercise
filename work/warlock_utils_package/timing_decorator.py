import time
import asyncio
from functools import wraps
import inspect


def timing_decorator(func):
    if inspect.iscoroutinefunction(func):  # Check if the function is async

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)  # Await the async function
            end_time = time.time()
            duration = end_time - start_time
            print(
                f"Async function '{func.__name__}' took {duration:.6f} seconds to complete."
            )
            return result

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            print(
                f"Sync function '{func.__name__}' took {duration:.6f} seconds to complete."
            )
            return result

        return sync_wrapper
