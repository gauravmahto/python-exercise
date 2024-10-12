import inspect


def decorator(func):
    if inspect.iscoroutinefunction(func):  # Check if the function is async

        async def wrapper(*args, **kwargs):
            print(f"Calling async function: {func.__name__}")
            result = await func(*args, **kwargs)
            print(f"Finished calling async function: {func.__name__}")
            return result

    else:

        def wrapper(*args, **kwargs):
            print(f"Calling function: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"Finished calling function: {func.__name__}")
            return result

    return wrapper


class Decorator:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwds):
        print(f"Calling function: {self.func.__name__}")
        result = self.func(*args, **kwds)
        print(f"Finished calling function: {self.func.__name__}")
        return result


if __name__ == "__main__":

    @decorator
    def say_hello(suffix):
        print(f"Hello {suffix}")

    say_hello("bye")

    @Decorator
    def another_printer(data):
        print(data)

    another_printer("Hello")
