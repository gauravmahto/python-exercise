import timeit
from multi_process import Process

from warlock_utils_package import timing_decorator


@timing_decorator
def squares():
    # List comprehension (faster)
    return [x**2 for x in range(100000000)]


@timing_decorator
def squares_2():
    squares = []
    # Equivalent using a loop (slower)
    for x in range(100000000):
        squares.append(x**2)

    return squares


if __name__ == "__main__":
    process_a = Process(target=squares)
    process_b = Process(target=squares_2)

    process_a.start()
    process_b.start()

    print("Performing next task in the main process")
    # Measuring the execution time of a list comprehension
    print(timeit.timeit("[x ** 2 for x in range(100000000)]", number=1))

    process_a.join()
    process_b.join()
