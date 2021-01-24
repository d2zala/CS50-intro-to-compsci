from sys import argv, exit
from cs50 import SQL

if len(argv) != 2:
    print("Usage: roster.py Gryffindor")
    exit(0)

db = SQL("sqlite:///students.db")

students_list = db.execute("SELECT first,middle,last,birth FROM students WHERE house = (?) ORDER BY last, first", argv[1])

for row in students_list:
    if row["middle"] == None:
        print(row["first"] + " " + row["last"] + ", born " + str(row["birth"]))
    else:
        print(row["first"] + " " + row["middle"] + " " + row["last"] + ", born " + str(row["birth"]))
