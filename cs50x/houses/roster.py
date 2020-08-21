import csv
import sys
from sys import argv
from cs50 import SQL

# Checks for correct usage
if len(argv) != 2:
    print("Usage: python roster.py housename")
    sys.exit()

# Opens SQL db
open("students.db", "r").close()
db = SQL("sqlite:///students.db")

# Checks for correct house
housename = argv[1].lower()
houses = ["gryffindor", "slytherin", "ravenclaw", "hufflepuff"]
if housename.lower() not in houses:
    print("Invalid Hogwarts house")
    sys.exit()

# SQL select
result = db.execute(f"SELECT * FROM students WHERE lower(house) = lower('{argv[1]}') ORDER BY last, first;")

# Prints results and prints middle name if applicable
for i in result:
    if i['middle']:
        middle = " " + i['middle']
    else:
        middle = ""
    print(f"{i['first']}{middle} {i['last']}, born {i['birth']}")