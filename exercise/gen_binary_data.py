import pickle

my_list = [1, 2, 3, 4, 'Hello how Are you?', 6, 7, 8, 9, 10]
my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

to_dump = input("Enter 'l' to dump a list (default), 'd' to dump a dictionary: ")
to_dump = to_dump.lower() if to_dump else 'l'

with open('data/binary_data.ignore.bin', "wb") as file:
    if to_dump == 'l':
        pickle.dump(my_list, file)
    else:
        pickle.dump(my_dict, file)
