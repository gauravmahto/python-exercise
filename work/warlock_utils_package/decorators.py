import asyncio
import inspect
from typing import Any


def decorator(func: callable) -> callable:
    """
    A decorator that prints out when a function is called and when it finished calling.

    The decorator will work with both sync and async functions.

    :param func: The function to be decorated. Can be either a sync or an async function.
    :return: The wrapper function.
    :rtype: callable
    """
    if inspect.iscoroutinefunction(func):  # Check if the function is async

        async def wrapper(*args, **kwargs) -> Any:
            """
            The wrapper function for async functions.

            :param args: The arguments to be passed to the function.
            :param kwargs: The keyword arguments to be passed to the function.
            :return: The result of calling the function.
            :rtype: Any
            """
            print(f"Calling async function: {func.__name__}")
            result = await func(*args, **kwargs)
            print(f"Finished calling async function: {func.__name__}")
            return result

    else:

        def wrapper(*args, **kwargs) -> Any:
            """
            The wrapper function for sync functions.

            :param args: The arguments to be passed to the function.
            :param kwargs: The keyword arguments to be passed to the function.
            :return: The result of calling the function.
            :rtype: Any
            """
            print(f"Calling function: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"Finished calling function: {func.__name__}")
            return result

    return wrapper


class Decorator:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwds):
        # Check if the function is a coroutine (async function)
        if inspect.iscoroutinefunction(self.func):

            async def async_wrapper(*args, **kwargs):
                print(f"Calling async function: {self.func.__name__}")
                result = await self.func(*args, **kwargs)
                print(f"Finished calling async function: {self.func.__name__}")
                return result

            # If called within an active event loop, use await directly
            if asyncio.get_running_loop().is_running():
                return async_wrapper(*args, **kwds)
            else:
                # If there's no event loop running, use asyncio.run()
                return asyncio.run(async_wrapper(*args, **kwds))

        else:
            print(f"Calling function: {self.func.__name__}")
            result = self.func(*args, **kwds)
            print(f"Finished calling function: {self.func.__name__}")
            return result


if __name__ == "__main__":

    async def main():

        @decorator
        def say_hello(suffix):
            print(f"Hello {suffix}")

        say_hello("bye")

        @Decorator
        async def another_printer(data):
            print(data)

        await another_printer("Hello")

    asyncio.run(main())
