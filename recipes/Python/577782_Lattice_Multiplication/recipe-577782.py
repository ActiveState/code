"""
    @file  lattice.py
    @brief multiplication of two numbers
"""

def lattice(valueA, valueB):
    """ the lattice calculation bases on a matrix writing
        the digits of the first value as column headers and
        writing the digits of the second value as row labels.
        Each matrix cell has a diagonal. Multiplicating the
        column digit with the row digit the result will be
        splitted like this: 9 x 8 = 72 -> 7 will written above
        the diagonal and 2 will be written below the diagonal.

        When each cell is filled - looking at the diagonals -
        you can see that - more or less - at the top right
        of a cell and at the bottom left the diagonal can be
        continued when there is a further cell. Starting at
        the bottom right of the matrix we sum up each digit
        of same diagonal.

        The last step is to adjust each sum that way that the
        value > 9 is transfered as "too much" to the next sum.
        Each time a digit remains being part of the final
        product of the multiplication. You have to start with
        the last diagonal (bottom right of matrix)
    """
    diagonals = [0] * (len(valueA) + len(valueB))
    for indexA, digitA in enumerate(valueA):
        for indexB, digitB in enumerate(valueB):
            value = int(digitA) * int(digitB)
            diagonals[indexA+indexB+0] += value // 10
            diagonals[indexA+indexB+1] += value %  10

    digits = []
    rest   = 0
    for value in reversed(diagonals):
        value += rest
        if value > 9:
            rest = value // 10
            digits.insert(0, value % 10)
        else:
            rest = 0
            digits.insert(0, value)

    if rest > 0:
        digits.insert(0, rest)

    if digits[0] == 0:
        del digits[0]
    return digits

def test():
    """ verifying lattice calculation """
    stringA = "1234567890"
    stringB = "1234567890"

    # python calculates:
    resultA = "%s" % (int(stringA) * int(stringB))
    print("%s x %s = %s" % (stringA, stringB, resultA))

    # string digits as input:
    resultB = lattice(stringA, stringB)
    assert resultB == list(map(int, resultA))

    # list of integer digits as input:
    resultC = lattice(list(map(int, stringA)), list(map(int, stringB)))
    assert resultC == list(map(int, resultA))

if __name__ == "__main__":
    test()
