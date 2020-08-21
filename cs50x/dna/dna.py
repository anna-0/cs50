from sys import argv
import sys
import csv


# Checks for correct usage
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit()

# Opens and reads sequence.txt
with open(argv[2], "r") as sequencefile:
    sequence = sequencefile.readline()

# Initialises list to put STR field names into
STRlist = []

# Opens and reads database.csv and puts header STRs into list
with open(argv[1], "r") as databasefile:
    database = csv.DictReader(databasefile)
    STRlist = database.fieldnames[1:]

# Initialises STR values dictionary with value baseline set explicitly to zero, otherwise not all results would be checked against when finding match
STRvalues = dict.fromkeys(STRlist, 0)

# Sets up to find repeats of STRs as were stipulated in field names STR list
for STR in STRlist:
    maxcount = 0
    L = len(STR)
    count = 0
    start = 0

    # Finds locations of STRs and checks if they repeat, and tallies up counter. Modified from https://stackoverflow.com/questions/51690245/consecutive-substring-in-python
    while True:
        loc = sequence.find(STR, start)
        if loc == -1:
            break
        if start != loc:
            count = 0
            count += 1
            start = loc + L
        else:
            count += 1
            start = loc + L

        # Sets maximum numbers of STRs found
        if count > maxcount:
            maxcount = count

        # Puts maximum counts into list with corresponding STRs
        STRvalues[STR] = maxcount

# Reopens database file and lists people and their values
with open(argv[1], "r") as databasefile:
    suspects = csv.DictReader(databasefile)

    # Counts up number of matches between maxcounts and people's numbers, prints if match
    for person in suspects:
        match = 0
        for STR in STRvalues:
            if STRvalues[STR] == int(person[STR]):
                match += 1
        if match == len(STRvalues):
            print(f"{person['name']}")
            sys.exit(0)
    
    # Print no match if none
    print("No match")
    sys.exit(1)