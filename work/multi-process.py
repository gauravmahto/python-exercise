from multiprocessing import Process, Value
import os

def cpu_bound_task(shared_count):
    for _ in range(10**6):  # Using a smaller count for illustration
        with shared_count.get_lock():  # Ensures mutual exclusion
            shared_count.value += 1

if __name__ == '__main__':
    # Create a shared integer value (starting at 0) between processes
    shared_count = Value('i', 0)  # 'i' means integer type

    processes = []
    for i in range(4):  # Start 4 processes
        process = Process(target=cpu_bound_task, args=(shared_count,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print(f"Final count: {shared_count.value}")
