# for randomness
from random import random

# minimum finder
def minimum(value_one, value_two):
    if value_one < value_two:
        return value_one
    return value_two

# main function
def simulate(boys, girls, years, total, fast):
    # make sure the ages are DIFFERENT
    b_ages = range(70)
    g_ages = range(70)
    # setup the ages
    for age in range(70):
        b_ages[age] = g_ages[age] = 0
    b_ages[20] = boys
    g_ages[20] = girls
    # simulator
    for year in range(years):
        # slow printer
        if not fast:
            print 'Year =', year
            sum = 0
            for age in range(70):
                sum += b_ages[age]
            print 'Boys =', sum
            sum = 0
            for age in range(70):
                sum += g_ages[age]
            print 'Girls =', sum
            print 'Boy Ages =', str(b_ages)[1:-1]
            print 'Girl Ages =', str(g_ages)[1:-1]
        # find out the number of offspring
        b_born = g_born = 0
        for age in range(20, 50):
            pairs = minimum(b_ages[age], g_ages[age])
            total_born = int(random() * (pairs + 1))
            half = int(random() * (total_born + 1))
            b_born += total_born - half
            g_born += half
        # make everyone age one year
        for age in range(68, -1, -1):
            b_ages[age + 1] = b_ages[age]
            g_ages[age + 1] = g_ages[age]
        # add the offspring
        b_ages[0] = b_born
        g_ages[0] = g_born
        # check for total population
        if total != 0:
            sum = 0
            for age in range(70):
                sum += b_ages[age] + g_ages[age]
            if total <= sum:
                break
        # pause for reading
        if not fast:
            raw_input('Pausing ...')
    # finish the simulation
    print 'Year =', year + 1
    sum = 0
    for age in range(70):
        sum += b_ages[age]
    print 'Boys =', sum
    sum = 0
    for age in range(70):
        sum += g_ages[age]
    print 'Girls =', sum
    print 'Boy Ages =', str(b_ages)[1:-1]
    print 'Girl Ages =', str(g_ages)[1:-1]
    # calculate the total
    sum = 0
    for age in range(70):
        sum += b_ages[age] + g_ages[age]
    print 'There are a total of', sum, 'people.'

# get input
def start():
    global notes_words
    loop = True
    while loop:
        try:
            boys = int(raw_input('How many boys should we start with? '))
            loop = False
        except:
            pass
    loop = True
    while loop:
        try:
            girls = int(raw_input('How many girls should we start with? '))
            loop = False
        except:
            pass
    loop = True
    while loop:
        try:
            years = int(raw_input('How many years should we simulate? '))
            loop = False
        except:
            pass
    loop = True
    while loop:
        try:
            total = int(raw_input('How many people do we want? '))
            loop = False
        except:
            pass
    # more vocabulary
    accept = ['yes', 'y', 'yeah', 'si']
    deny = ['no', 'n', 'nada', 'never']
    loop = True
    while loop:
        try:
            fast = raw_input('Should we go fast? ')
            if fast.lower() in accept:
                fast = True
                loop = False
            elif fast.lower() in deny:
                fast = False
                loop = False
            elif fast.lower() in notes_words:
                print 'The available commands are ' + str(accept)[1:-1] + ', ' \
                      + str(deny)[1:-1] + ', ' + str(notes_words)[1:-1] + '.'
            else:
                print '"' + fast + '" is not something that I understand.'
        except:
            pass
    try:
        simulate(boys, girls, years, total, fast)
    except:
        print 'The simulation crashed !!!'

# define the vocabulary
start_words = ['start', 'begin', 'exe', 'execute']
break_words = ['break', 'exit', 'end', 'quit']
notes_words = ['help', '?', '/?', '-?']

# get command
print 'Executing Population Simulator ...'
while True:
    prompt = raw_input('Please enter a command: ')
    if prompt.lower() in start_words:
        start()
    elif prompt.lower() in break_words:
        break
    elif prompt.lower() in notes_words:
        print 'The available commands are ' + str(start_words)[1:-1] + ', ' + \
              str(break_words)[1:-1] + ', ' + str(notes_words)[1:-1] + '.'
    else:
        print '"' + prompt + '" is not something that I understand.'
