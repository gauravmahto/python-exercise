import pickle

my_list = [1, 2, 3, 4, 'Hello how Are you?', 6, 7, 8, 9, 10]

with open('data/binary_data.ignore.bin', "wb") as file:
    pickle.dump(my_list, file)
