from array import array
from random import Random

class BloomFilter:
    # http://en.wikipedia.org/wiki/Bloom_filter

    def __init__(self, num_bits, num_probes, probe_func):
        self.num_bits= num_bits
        num_words = (num_bits + 31) // 32
        self.arr = array('L', [0]) * num_words
        self.num_probes = num_probes
        self.probe_func = get_probes

    def add(self, key):
        for i, mask in self.probe_func(self, key):
            self.arr[i] |= mask

    def match_template(self, bfilter):
        return (self.num_bits == bfilter.num_bits \
            and self.num_probes == bfilter.num_probes \
            and self.probe_func == bfilter.probe_func)

    def union(self, bfilter):
        if self.match_template(bfilter):
            self.arr = [a | b for a, b in zip(self.arr, bfilter.arr)]
        else:
            # Union b/w two unrelated bloom filter raises this
            raise ValueError("Mismatched bloom filters")

    def intersection(self, bfilter):
        if self.match_template(bfilter):
            self.arr = [a & b for a, b in zip(self.arr, bfilter.arr)]
        else:
            # Intersection b/w two unrelated bloom filter raises this
            raise ValueError("Mismatched bloom filters")

    def __contains__(self, key):
        return all(self.arr[i] & mask for i, mask in self.probe_func(self, key))

def get_probes(bfilter, key):
    hasher = Random(key).randrange
    for _ in range(bfilter.num_probes):
        array_index = hasher(len(bfilter.arr))
        bit_index = hasher(32)
        yield array_index, 1 << bit_index

if __name__ == '__main__':

    from random import sample
    from string import ascii_letters

    states = '''Alabama Alaska Arizona Arkansas California Colorado Connecticut
        Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas
        Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota
        Mississippi Missouri Montana Nebraska Nevada NewHampshire NewJersey
        NewMexico NewYork NorthCarolina NorthDakota Ohio Oklahoma Oregon
        Pennsylvania RhodeIsland SouthCarolina SouthDakota Tennessee Texas Utah
        Vermont Virginia Washington WestVirginia Wisconsin Wyoming'''.split()

    bf = BloomFilter(num_bits=1000, num_probes=14, probe_func=get_probes)
    for state in states:
        bf.add(state)

    m = sum(state in bf for state in states)
    print('%d true positives out of %d trials' % (m, len(states)))

    trials = 100000
    m = sum(''.join(sample(ascii_letters, 5)) in bf for i in range(trials))
    print('%d true negatives and %d false negatives out of %d trials'
          % (trials-m, m, trials))
