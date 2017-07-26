from itertools import tee, chain, islice, groupby
from heapq import merge

def hamming_numbers():
    # Generate "5-smooth" numbers, also called "Hamming numbers"
    # or "Regular numbers".  See: http://en.wikipedia.org/wiki/Regular_number
    # Finds solutions to 2**i * 3**j * 5**k  for some integers i, j, and k.

    def deferred_output():
        'Works like a forward reference to the "output" global variable'
        for i in output:
            yield i

    result, p2, p3, p5 = tee(deferred_output(), 4)  # split the output streams
    m2 = (2*x for x in p2)                          # multiples of 2
    m3 = (3*x for x in p3)                          # multiples of 3
    m5 = (5*x for x in p5)                          # multiples of 5
    merged = merge(m2, m3, m5)
    combined = chain([1], merged)                   # prepend starting point
    output = (k for k, v in groupby(combined))      # eliminate duplicates

    return result


if __name__ == '__main__':
    print(list(islice(hamming_numbers(), 1000)))    # Show first 1000 hamming numbers
