#!/usr/bin/env python

"""Sudoku solver

usage: python sudoku.py <file> [<depth>]

The input file should contain exactly 81 digits, with emtpy fields marked
with 0. Optionally, dots (.) may be used for empty fields if better
readability is required. All other characters are discarded.

The default guessing depth is 2.

"""


import pprint
from itertools import chain


def parseString(text):
    s = text.replace('.', '0')
    s = [int(x) for x in s if x.isdigit()]
    s = [s[i:i+9] for i in range(0, 81, 9)]
    return s


def parse(name):
    f = open(name)
    s = f.read()
    f.close()
    return parseString(s)


class NotSolvable(Exception):

    """Not solvable"""

    pass


class IncorrectSolution(Exception):
    
    """Incorrect solution"""

    pass


class Done(Exception):

    """Done!"""

    pass


# These constants are speed optimizations for use in loops
MASK9 = set(range(1, 10))
NINE = tuple(range(9))
THREE = tuple(range(3))


def try_cross_and_region(matrix, depth=0):
    """Fill cells unambiguously determined by their lines and regions.
    
    For every empty cell, find the values of known digits in its row, column,
    and region. If there is exactly one digit left, it is the value of the
    cell. If there are more and if search depth is non-zero, try solving the
    puzzle for each of the values.
    
    """
    result = False
    for col in NINE:
        yexist = set(m[col] for m in matrix)
        rcol = col // 3
        rcol3 = 3 * rcol
        rcol3p3 = rcol3 + 3
        for row in NINE:
            if not matrix[row][col]:
                xexist = set(matrix[row])
                rrow = row // 3
                rrow3 = 3 * rrow
                region = [matrix[rrow3+i][rcol3:rcol3p3] for i in THREE]
                rexist = set(chain(*region))
                missing = MASK9 - xexist - yexist - rexist
                size = len(missing)
                if size == 1:
                    elem = list(missing)[0]
                    matrix[row][col] = elem
                    yexist.add(elem)  # Speed optimization, see outer loop
                    result = True
                elif size == 0:
                    raise NotSolvable()
                elif size < 4 and depth > 0:
                    # The size limit was established by experimentation.
                    hypothesize(matrix, row, col, missing, depth-1)
    return result


def try_adjacent_lines(matrix):
    """Fill cells unambiguously determined by same-region lines.
    
    For every empty cell, find the values of known digits in the lines passing
    through the same region. For the cell's line, the other two values in the
    region should be known. For the remaining two lines, all digits in the
    other two regions should be known. There should be exactly one value
    happening twice on the other lines and not at all on the current line.
    It is the value of the current cell.

    If the above failed in one direction, try the other.

    If both horizontal and vertical searches failed for a given cell but all
    24 other-region values are known, there should be exactly one value
    happening 4 times (each for one of the other regions checked). It is the
    value of the current cell.
    
    """
    result = False
    for col in NINE:
        rcol = col // 3
        rcol3 = 3 * rcol
        rcol3p3 = rcol3 + 3
        othercolidxs = (rcol3 + (col+1)%3, rcol3 + (col+2)%3)
        for row in NINE:
            if not matrix[row][col]:
                rrow = row // 3
                rrow3 = 3 * rrow
                otherrows = (rrow3 + (row+1)%3, rrow3 + (row+2)%3)
                otherrows = [matrix[orow] for orow in otherrows]
                othercols = [[m[ocol] for m in matrix]
                             for ocol in othercolidxs]
                othercross = []  # Container for other-region known values
                if _check_other_lines2(matrix, rcol, row, col, matrix[row],
                                       otherrows, othercross):
                    result = True
                elif _check_other_lines2(matrix, rcol, row, col,
                                         [m[col] for m in matrix],
                                         othercols, othercross):
                    result = True
                elif len(othercross) == 24:
                    fours = [i for i in MASK9 if othercross.count(i) == 4]
                    if fours:
                        matrix[row][col] = fours[0]
                        result = True
    return result


def _check_other_lines2(matrix, ridx, row, col, line, otherlines, othercross):
    """Helper function for try_adjacent_lines().

    Check the values in one direction. As an artifact, known digit values
    from the lines are collected into othercross.
    
    """
    ridx3 = 3 * ridx
    ridx3p3 = ridx3 + 3
    line = line[ridx3:ridx3p3]
    if line.count(0) != 1:
        return False
    allfields = []
    for other in otherlines:
        other = list(other)
        del other[ridx3:ridx3p3]
        allfields += other
    if allfields.count(0):
        return False
    othercross += allfields
    twos = set(i for i in MASK9 if allfields.count(i) == 2)
    twos -= set(line)
    if len(twos) == 1:
        elem = list(twos)[0]
        if elem not in line:
            matrix[row][col] = elem
            return True
    return False


# Speed optimization in for loop
RLOCATIONS = set((row, col) for row in THREE for col in THREE)


def try_masking(matrix):
    """Fill cells that remain alone after "masking" by other cells.

    For each digit value, "stamp out" the puzzle to see which regions have
    empty cells that could potentially still be filled with that value. For
    regions with single cells left, fill those cells with the value.
    
    Known problems:
    This function causes a 'Bad call' exception in the profile module
    (see http://www.python.org/sf/1117670) in some Python installations.
    
    """
    result = False
    for digit in MASK9:
        locations = set(RLOCATIONS)
        matrix2 = [list(m) for m in matrix]
        for row in NINE:
            try:
                idx = matrix2[row].index(digit)
            except ValueError:
                idx = -1
            else:
                matrix2[row] = [-1 for col in NINE]
                for row2 in NINE:
                    matrix2[row2][idx] = -1
                locations.discard((row//3, idx//3))
        for rrow, rcol in locations:
            rcol3 = 3 * rcol
            rcol3p3 = rcol3 + 3
            rrow3 = 3 * rrow
            region2 = (matrix2[rrow3+i][rcol3:rcol3p3] for i in THREE)
            region2 = [x for x in chain(*region2)]
            if region2.count(0) == 1:
                idx = region2.index(0)
                row = rrow3 + idx // 3
                col = rcol3 + idx % 3
                matrix[row][col] = digit
                result = True
    return result


def hypothesize(matrix, row, col, values, depth):
    """Try further search with the specified cell equal to each of values."""
    for x in values:
        matrix2 = [list(m) for m in matrix]
        matrix2[row][col] = x
        try:
            solve(matrix2, depth)
        except (NotSolvable, IncorrectSolution):
            pass


def check_done(matrix):
    if 0 in chain(*matrix):
        return False
    for row in matrix:
        if len(set(row)) < 9:
            raise IncorrectSolution()
    for col in range(9):
        col = set(m[col] for m in matrix)
        if len(col) < 9:
            raise IncorrectSolution()
    for rrow in range(3):
        for rcol in range(3):
            region = [matrix[3*rrow+i][3*rcol:3*(rcol+1)] for i in range(3)]
            if len(set(chain(*region))) < 9:
                raise IncorrectSolution()
    return True


def solve(matrix, depth=2):
    while try_cross_and_region(matrix):
        pass
    if check_done(matrix):
        pprint.pprint(matrix)
        raise Done()
    
    while try_adjacent_lines(matrix):
        pass
    if check_done(matrix):
        pprint.pprint(matrix)
        raise Done()
    
    while try_masking(matrix):
        pass
    if check_done(matrix):
        pprint.pprint(matrix)
        raise Done()
    
    while try_cross_and_region(matrix, depth=depth):
        pass
    if check_done(matrix):
        pprint.pprint(matrix)
        raise Done()


if __name__ == "__main__":
    import sys
    matrix = parse(sys.argv[1])
    depth = 2
    if len(sys.argv) > 2:
        depth = int(sys.argv[2])
    try:
        solve(matrix, depth)
        print "Failed, this is all I could fill in:"
        pprint.pprint(matrix)
    except Done:
        print "Done!"
    except NotSolvable:
        print "Not solvalbe, this is how I filled it in:"
        pprint.pprint(matrix)
    import os
    utime, stime, cutime, cstime, elapsed = os.times()
    print "cputime=%s" % (utime + stime)

# vim:et:ai:sw=4
