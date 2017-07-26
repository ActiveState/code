from decimal import Decimal, getcontext
from random import randint

# Return 3 decimal places

getcontext().prec = 3

# Function "get_input" verifies the input. As "raw_input" does not accept an int
# as input (which is what we need), the function converts the input into a str
# and checks whether the str is a digit. If so it converts the str to an int and
# returns it. If not the user is prompted again for an input. A float is not a
# valid input ("isdigit" would not be True). You can convert an int to a str but
# not a float to a str. The return value is used to define the number of trials.

def get_input(prompt):
    ''' (str) --> int
    Ask the user for input, convert it into a str, check for a digit and convert
    into an int. Prompt as long as the user provides a valid input.
    '''
    trials = raw_input(prompt)
    trials = str(trials)
    while not trials.isdigit():
        print "You have to provide an integer for the number of flips!"
        trials = raw_input(prompt)
    return int(trials)

heads = 0
tail = 0
i = 0

print "\n"

flip = get_input("How often shall I flip a coin? ")

print "\nFlipping the coin ..."

while i < int(flip):
    coin = randint(1,2)
    if coin == 1:
        heads += 1
    else:
        tail += 1
    i += 1

relfreq_heads = Decimal(heads) / Decimal(int(flip))
relfreq_tail = Decimal(tail) / Decimal(int(flip))  

print "\nFlipping a coin", flip, "times yields:\n"

print "Outcome\t\tFrequency\tRelative Frequency"
print "=======\t\t=========\t=================="
print "Heads\t\t", heads, "\t\t", relfreq_heads
print "Tail\t\t", tail, "\t\t", relfreq_tail
