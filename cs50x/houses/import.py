import csv
from cs50 import SQL
import sys
from sys import argv

# Checks for correct usage
if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    sys.exit()

# Opens database in SQL
open("students.db", "w").close()
db = SQL("sqlite:///students.db")

# Creates student table
db.execute("CREATE TABLE students(first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# Iterates csv into table
with open(argv[1], "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        
        # Checks for middle name and uses more columns if so
        fullname = row['name']
        names = fullname.split()
        if len(names) == 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)",
                       names[0], names[1], names[2], row["house"], row["birth"])
        elif len(names) == 2:
            db.execute("INSERT INTO students(first, last, house, birth) VALUES(?,?,?,?)",
                       names[0], names[1], row["house"], row["birth"])