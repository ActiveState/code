NUM_SAILORS = 5
NUM_ITERATIONS = 6
UPPER_BOUND = 1000000

def check(pile, verbose=False):
    for i in range(0, NUM_ITERATIONS):
        share, monkey = divmod(pile, NUM_SAILORS)
        if monkey == 1:
            new_pile = pile - (share + monkey)
            if verbose:
                print ("%d: share [%d] monkey [%d] new_pile [%d]" % (pile, share, monkey, new_pile))
            pile = new_pile
        else:
            return False
    return True   

def solve(upper_bound):
    for x in range(1, upper_bound):
        if check(x):
            return x
    return 0

if __name__ == "__main__":
    x = solve(UPPER_BOUND)
    if x:
        print ("Solution: %d" % x)
        check(x, True)
    else:
        print ("No solution < %d" % UPPER_BOUND)
