def Trailing_Zeroes(x):
    fives = 0
    for number in range(2, x+1):          
        while number > 0:
            if number % 5 == 0:
                fives += 1
                number = number/5
            else:
                break
    return fives
