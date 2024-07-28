import pickle

with open('data/binary_data.ignore.bin', "rb") as file:
    my_list = pickle.load(file)
    print(my_list)
