__author__ = 'Ethan D. Hann'

import math

print("Is your number a perfect square?! Find out now!")
print("Or you can square a number!")

#Setting up while loop with loop-controlled variable
x = 1
while x > 0:

#Get input from user
        op = input("q -> quit program \n" \
                   "c -> checks a number \n" \
                   "s -> squares a number \n")
#Check if input is c, s, or q
        if op[0] is "c":
#If c, take the square root of the number and round it to the largest integer value less than or equal to x: math.floor(x)
                num = input("Enter a whole number (q -> quit): ")
                sNum = math.floor(math.sqrt(int(num)))
                numSquared = sNum * sNum
                
#If, else statement to determine if numSquared is equal to the input. 
                if numSquared == int(num):
                    print(num, "IS a perfect square! \n"\
                            "√("+ num + ") =", math.sqrt(int(num)))
                else:
                    print(num, "is NOT a perfect square! \n" \
                            "√("+ num + ") =", math.sqrt(int(num)))
#If s, simply square user's input
        if op[0] is "s":
                num = int(input("Enter a number to square (q -> quit): "))
                numSquared = num ** 2
                print(num, "squared is", numSquared)

#If q, quit program with goodbye message
        else:
                if op[0] is 'q':
                        x -= 1
                        print("Goodbye!")
                else:
                        print("Must enter either c, s, or q")
