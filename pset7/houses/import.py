from cs50 import SQL
from sys import argv, exit
import csv

if len(argv) != 2:
    print("Usage: import.py characters.csv")
    exit(0)
if argv[1].endswith(".csv") == False:
    print("Usage: import.py characters.csv")
    exit(1)

file_name = argv[1]
#open(file_name, "r").close()
db = SQL("sqlite:///students.db")


with open(file_name, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["name"]
        name_split = name.split()
        if len(name_split) == 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES (?,?,?,?,?)",
                       name_split[0], name_split[1], name_split[2], row["house"], row["birth"])
        else:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES (?,?,?,?,?)",
                       name_split[0], None, name_split[1], row["house"], row["birth"])
