import csv
import io

with open("data/Batting/ODI data.csv", "r", encoding="utf-8") as file:
    content = file.read()

# Use io.StringIO to convert the string data to a file-like object
csvfile = io.StringIO(content)
csv_reader = csv.reader(csvfile)

for row in csv_reader:
    print(row)
else:
    print("An error occurred:")
    print(content)
