def is_straight(hand, numwildcards=0):
    """Checks for a five card straight

    Inputs: list of non-wildcards plus wildcard count
        2,3,4, ... 10, 11 for Jack, 12 for Queen,
        13 for King, 14 for Ace
        Hand can be any length (i.e. it works for seven card games).

    Outputs:  highest card in a five card straight
              or 0 if not a straight.
        Original list is not mutated.
        Ace can also be a low card (i.e. A2345).

    >>> is_straight([14,2,3,4,5])
    5
    >>> is_straight([14,2,3,4,6])
    0
    >>> is_straight([10,11,12,13,14])
    14
    >>> is_straight([2,3,5], 2)
    6
    >>> is_straight([], 5)
    14
    >>> is_straight([2,4,6,8,10], 3)
    12
    >>> is_straight([2,4,4,5,5], 2)
    6
    """

    hand = set(hand)
    if 14 in hand:
        hand.add(1)
    for low in (10,9,8,7,6,5,4,3,2,1):
        needed = set(range(low, low+5))
        if len(needed - hand) <= numwildcards:
            return low+4
    return 0



def groups(hand, numwildcards=0):
    """Checks for pairs, threes-of-a-kind, fours-of-a-kind,
       and fives-of-a-kind

    Inputs: list of non-wildcards plus wildcard count
        2,3,4, ... 10, 11 for Jack, 12 for Queen,
        13 for King, 14 for Ace
        Hand can be any length (i.e. it works for seven card games)
    Output: tuple with counts for each value (high cards first)
        for example (3, 14), (2, 11)  full-house Aces over Jacks
        for example (2, 9), (2, 7)    two-pair Nines and Sevens
    Maximum count is limited to five (there is no seven of a kind).
    Original list is not mutated.

    >>> groups([11,14,11,14,14])
    [(3, 14), (2, 11)]
    >>> groups([7, 9, 10, 9, 7])
    [(2, 9), (2, 7)]
    >>> groups([11,14,11,14], 1)
    [(3, 14), (2, 11)]
    >>> groups([9,9,9,9,8], 2)
    [(5, 9), (2, 8)]
    >>> groups([], 7)
    [(5, 14), (2, 13)]
    """

    result = []
    counts = [(hand.count(v), v) for v in range(2,15)]
    for c, v in sorted(counts, reverse=True):
        newcount = min(5, c + numwildcards) # Add wildcards upto five
        numwildcards -= newcount - c        # Wildcards remaining
        if newcount > 1:
            result.append((newcount, v))
    return result



import doctest
print doctest.testmod()
