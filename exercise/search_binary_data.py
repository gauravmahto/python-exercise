import pickle
from typing import List, Dict

with open("data/binary_data.ignore.bin", "rb") as file:
    my_data = pickle.load(file)
    print(my_data)

int_to_search = int(input("Enter a number to search"))

found = False

if isinstance(my_data, List):
    print("The loaded data is a list")

    for i in range(len(my_data)):
        if my_data[i] == int_to_search:
            print(f"Found {int_to_search} in the list at index {i}")
            found = True
            break

elif isinstance(my_data, Dict):
    print("The loaded data is a dictionary")

    for key in my_data.keys():
        if my_data[key] == int_to_search:
            print(f"Found {int_to_search} in the dictionary at key {key}")
            found = True

else:
    print("The binary data is not a list or a dictionary")

if not found:
    print(f"Not found {int_to_search} in the list")
