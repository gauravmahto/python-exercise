with open("data/words.txt", "r") as file:
    data = file.read()

    data = data.replace(input("Enter word to replace: "), input("Enter new word: "))

    with open("data/words_updated.ignore.txt", "w") as file_updated:
        file_updated.write(data)
