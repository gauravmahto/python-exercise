def count_words_and_chars(line):
    words = line.split()
    str = ""
    return len(words), len(str.join(words))


with open("data/words.txt", "r") as file:
    data = file.readlines()

    total_words = 0
    total_chars = 0
    total_line = 0

    for line in data:
        line = line.strip()
        if line == "":
            continue

        words, chars = count_words_and_chars(line)
        total_words += words
        total_chars += chars
        total_line += 1

print(
    f"There are {total_words} words and {total_chars} characters and {total_line} lines in the file."
)
