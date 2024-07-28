with open('data/words.txt', "r") as file:
      data = file.read()
      with open('data/words_copy.ignore.txt', "w") as file_copy:
        file_copy.write(data)
