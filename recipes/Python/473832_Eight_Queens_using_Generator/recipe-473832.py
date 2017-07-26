import sys, itertools
from sets import Set

NUM_QUEENS = 8

MAX = NUM_QUEENS * NUM_QUEENS

# Each position (i.e. square) on the chess board is assigned a number
# (0..63). non_intersecting_table maps each position A to a set
# containing all the positions that are *not* attacked by the position
# A.

intersecting_table = {}
non_intersecting_table = {}

# Utility functions for drawing chess board
def display(board):
    "Draw an ascii board showing positions of queens"
    assert len(board)==MAX
    it = iter(board)
    for row in xrange(NUM_QUEENS):
        for col in xrange(NUM_QUEENS):
            print it.next(),
        print '\n'

def make_board(l):
    "Construct a board (list of 64 items)"
    board = [x in l and '*' or '_' for x in range(MAX)]
    return board

# Construct the non-intersecting table

for pos in range(MAX):
    intersecting_table[pos] = []

for row in range(NUM_QUEENS):
    covered = range(row * NUM_QUEENS, (row+1) * NUM_QUEENS)
    for pos in covered:
        intersecting_table[pos] += covered

for col in range(NUM_QUEENS):
    covered = [col + zerorow for zerorow in range(0, MAX, NUM_QUEENS)]
    for pos in covered:
        intersecting_table[pos] += covered

for diag in range(NUM_QUEENS):
    l_dist = diag + 1
    r_dist = NUM_QUEENS - diag
    
    covered = [diag + (NUM_QUEENS-1) * x for x in range(l_dist)]
    for pos in covered:
        intersecting_table[pos] += covered

    covered = [diag + (NUM_QUEENS+1) * x for x in range(r_dist)]
    for pos in covered:
        intersecting_table[pos] += covered


for diag in range(MAX - NUM_QUEENS, MAX):
    l_dist = (diag % NUM_QUEENS) + 1
    r_dist = NUM_QUEENS - l_dist + 1

    covered = [diag - (NUM_QUEENS + 1) * x for x in range(l_dist)]
    for pos in covered:
        intersecting_table[pos] += covered

    covered = [diag - (NUM_QUEENS - 1) * x for x in range(r_dist)]
    for pos in covered:
        intersecting_table[pos] += covered

universal_set = Set(range(MAX))

for k in intersecting_table:
    non_intersecting_table[k] = universal_set - Set(intersecting_table[k])

# Once the non_intersecting_table is ready, the 8 queens problem is
# solved completely by the following method. Start by placing the
# first queen in position 0. Every time we place a queen, we compute
# the current non-intersecting positions by computing union of
# non-intersecting positions of all queens currently on the
# board. This allows us to place the next queen.

def get_positions(remaining=None, depth=0):
    m = depth * NUM_QUEENS + NUM_QUEENS

    if remaining is not None:
        rowzone = [x for x in remaining if x < m]
    else:
        rowzone = [x for x in range(NUM_QUEENS)]

    for x in rowzone:
        if depth==NUM_QUEENS-1:
            yield (x,)
        else:
            if remaining is None:
                n = non_intersecting_table[x]
            else:
                n = remaining & non_intersecting_table[x]

            for p in get_positions(n, depth + 1):
                yield (x,) + p
    return

rl = [x for x in get_positions()]

for i,p in enumerate(rl):
   print '=' * NUM_QUEENS * 2, "#%s" % (i+1)
   display(make_board(p))

print '%s solutions found for %s queens' % (i+1, NUM_QUEENS)
