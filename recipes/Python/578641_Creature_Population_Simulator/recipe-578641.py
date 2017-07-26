def main():
    while True:
        creatures = get_creatures()
        years = get_years()
        summary = get_summary()
        target = get_target()
        simulate(creatures, years, summary, target)
        if get_exit():
            return

def get_creatures():
    while True:
        try:
            creatures = int(raw_input('How many creatures do you want to start with? '))
            if creatures > 0:
                return creatures
            print 'There must be at least one creature.'
        except:
            print 'You must enter a number.'

def get_years():
    while True:
        try:
            years = int(raw_input('How many years do you want simulated? '))
            if years > 0:
                return years
            print 'At least one year must be simulated.'
        except:
            print 'You must enter a number.'

def get_summary():
    while True:
        try:
            answer = raw_input('Do you want a summary of the simulation? ').lower()
            if answer == 'yes':
                return True
            if answer == 'no':
                return False
        except:
            pass
        print 'You must enter "yes" or "no".'

def get_target():
    while True:
        try:
            target = int(raw_input('What is the target population (0 for None)? '))
            if target > 0:
                return target
            return 0
        except:
            print 'You must enter a number.'

def simulate(creatures, years, summary, target):
    print
    divisions = [0 for division in range(21)]
    divisions[20] = creatures
    for year in range(years):
        if not summary:
            print 'It is year', year, 'and the divisions are as follows:'
            print str(divisions)[1:-1]
        children = divisions[20] / 2
        divisions[20] += divisions[19]
        for division in range(19):
            divisions[19 - division] = divisions[18 - division]
        divisions[0] = children
        if target:
            total = 0
            for division in range(21):
                total += divisions[division]
            if total >= target:
                break
    print 'It is year', year + 1, 'and the divisions are as follows:'
    print str(divisions)[1:-1]
    total = 0
    for division in range(21):
        total += divisions[division]
    print 'There are a total of', total, 'creatures.'
    print

def get_exit():
    while True:
        try:
            answer = raw_input('Do you wish to exit this program? ').lower()
            if answer == 'yes':
                return True
            if answer == 'no':
                return False
        except:
            pass
        print 'You must enter "yes" or "no".'

if __name__ == '__main__':
    main()
