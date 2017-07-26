def roundRobin(units, sets=None):
    """ Generates a schedule of "fair" pairings from a list of units """
    if len(units) % 2:
        units.append(None)
    count    = len(units)
    sets     = sets or (count - 1)
    half     = count / 2
    schedule = []
    for turn in range(sets):
        pairings = []
        for i in range(half):
            pairings.append(units[i], units[count-i-1])
        units.insert(1, units.pop())
        schedule.append(pairings)
    return schedule

""" test code """
if __name__ == '__main__':
    for pairings in roundRobin(range(5)):
        print pairings
