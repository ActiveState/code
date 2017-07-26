 import random

min=1
max=12

roll_again = 'yes'

die1=random.randint(min,max)
die2=random.randint(min,max)

while roll_again == 'yes' or roll_again == 'y':
    die1=random.randint(min,max)
    die2=random.randint(min,max)
    print ('shake, shake, shake!')
    print ('you got a:')
    print die1
    print die2

    print ('the sum of your two numbers are below:')
    print die1 + die2
    roll_again = raw_input ('roll the dice again')
