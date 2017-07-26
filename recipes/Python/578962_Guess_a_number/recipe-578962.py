__author__ = 'Benoit'
# guess a number between 1 and 100 in ten tries
import random
answer = 'yes'
while answer == "yes":
    NumToGuess = random.randint(1, 100)
    NumOfTry = 10
    print ("Try to guess a number between 1 and 100 in 10 tries")
    while NumOfTry != 0:
        try:
            x = int (input ("Please enter a number between 1 and 100"))
            if x > NumToGuess:
                print (x,"is too high")
                NumOfTry = NumOfTry - 1
                print (NumOfTry, "attempt(s) left")
                print ("")
            elif x < NumToGuess:
                print (x,"is too low")
                NumOfTry = NumOfTry - 1
                print (NumOfTry, "attempt(s) left")
                print ("")
            elif x == NumToGuess:
                print ("You Win, Congratulations!!!")
                NumOfTry = 0
        except:
            print ("Please enter a valid number. For example 1, 5 an 44 are valid numbers to input.")
    else:
        print ("The number to guess was: ", NumToGuess)
        answer = input ('Do you want to play again? (yes/no)')
else:
    print ("Thank you for playing. Goodbye")
