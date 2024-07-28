from file_handling import read_file_safe

def JTOI(text):
  text = text.replace('J', 'I')
  text = text.replace('j', 'i')
  return text

(success, data) = read_file_safe('../data/words.txt')

if success:
    print(JTOI(data))
else:
    print(data)
