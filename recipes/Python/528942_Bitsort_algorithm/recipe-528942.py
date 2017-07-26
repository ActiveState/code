# Python implementation of bitsort algorithm from "Programming Pearls"

def bitsort(filename, maxn):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn """

    # Initialize bitmap
    a = [0]*maxn

    # Read from file and fill bitmap
    for line in file(filename):
        n = int(line.strip())
        # Turn bits on for numbers
        if n<maxn: a[n] = 1

    # Return a generator that iterates over the list
    for n in range(len(a)):
        if a[n]==1: yield n

    
if __name__=="__main__":
    # numbers.txt should contain a list of numbers
    # each less than 1000000, one per line.
    for num in bitsort('numbers.txt',1000000):
        print num
