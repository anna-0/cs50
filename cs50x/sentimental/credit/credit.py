from cs50 import get_string


def main():
    
    # Gets card number from user
    while True:
        cardnumber = get_string("Card number: ")
        if len(str(cardnumber)) > 0 and int(cardnumber):
            break
    validate(cardnumber)
    
    
def validate(cardnumber):
    
    # Checks length is 13 or 15 or 16
    cardlength = len(str(cardnumber))
    if cardlength != 13 and cardlength != 15 and cardlength != 16:
        print("INVALID")
        return 1
    
    # Initialises sums
    firstsum = 0
    secondsum = 0
    checksum = 0 
    
    # For 16 digit (even) card numbers
    if cardlength % 2 == 0:
        for i in range(cardlength):
            n = int(cardnumber[i])
            
            # Finds every other number to multiply by 2
            if i % 2 == 0:
                digitx2 = n * 2
                
                # Takes each digit of 2 digit results
                if digitx2 >= 10:
                    firstsum += digitx2 % 10
                    firstsum += digitx2 // 10
                else:
                    firstsum += digitx2
            
            # Adds up other numbers
            else:
                secondsum += n

    # For 13 and 15 (odd) digit card numbers
    else:
        for i in range(cardlength):
            n = int(cardnumber[i])
            if i % 2 == 1:
                digitx2 = n * 2
                if digitx2 >= 10:
                    firstsum += digitx2 % 10
                    firstsum += digitx2 // 10
                else:
                    firstsum += digitx2
            else:
                secondsum += n

    # Checks Luhn validity
    checksum = (firstsum + secondsum) % 10
    
    # Determines which card
    if checksum == 0:
        if cardlength == 15:
            print("AMEX")
        elif cardlength == 16 and int(cardnumber[0]) == 5:
            print("MASTERCARD")
        elif int(cardnumber[0]) == 4:
            print("VISA")
    else:
        print("INVALID")


main()