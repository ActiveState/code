_nibbles = {"0":"0000", "1":"0001", "2":"0010", "3":"0011",
            "4":"0100", "5":"0101", "6":"0110", "7":"0111",
            "8":"1000", "9":"1001", "A":"1010", "B":"1011",
            "C":"1100", "D":"1101", "E":"1110", "F":"1111",
            "-":"-"}

def toBase2(number):
    """toBase2(number): given an int/long, converts it to
    a string containing the number in base 2."""
    # From a suggestion by Dennis Lee Bieber.
    if number == 0:
        return "0"
    result = [_nibbles[nibble] for nibble in "%X"%number]
    result[number<0] = result[number<0].lstrip("0")
    return "".join(result)


# Small test:
for i in xrange(-20, 21):
    print toBase2(i)
for i in xrange(-1000, 1000):
    if i != int(toBase2(i),2):
        print "Different"
