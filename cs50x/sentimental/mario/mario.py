from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

for rows in range(0, height):
    for spaces in range(1, height - rows):
        print(" ", end="")
    for lHashes in range(height - rows, height + 1):
        print("#", end="")
    print("  ", end="")
    for rHashes in range(height - rows, height + 1):
        print("#", end="")
    print()
