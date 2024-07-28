import pickle

with open("data/binary_data.ignore.bin", "rb") as file:
    my_list = pickle.load(file)
    with open("data/binary_data_copy.ignore.bin", "wb") as file_copy:
        pickle.dump(my_list, file_copy)
