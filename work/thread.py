import threading
import time

def print_numbers():
  for i in range(10):
    print(i)
    time.sleep(1)

def print_letters():
  for letter in "abcde":
    print(letter)
    time.sleep(1)

t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

t1.start()
t2.start()

t1.join()
t2.join()

print("Done")
