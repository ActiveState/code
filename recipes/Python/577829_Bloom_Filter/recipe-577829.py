from random import Random

class BloomFilter:
    # http://en.wikipedia.org/wiki/Bloom_filter

    def __init__(self, num_bytes, num_probes, iterable=()):
        self.array = bytearray(num_bytes)
        self.num_probes = num_probes
        self.num_bins = num_bytes * 8
        self.update(iterable)

    def get_probes(self, key):
        random = Random(key).random
        return (int(random() * self.num_bins) for _ in range(self.num_probes))

    def update(self, keys):
        for key in keys:
            for i in self.get_probes(key):
                self.array[i//8] |= 2 ** (i%8)

    def __contains__(self, key):
        return all(self.array[i//8] & (2 ** (i%8)) for i in self.get_probes(key))


##  Sample application  ##############################################

class SpellChecker(BloomFilter):

    def __init__(self, wordlistfiles, estimated_word_count=125000):
        num_probes = 14           # set higher for fewer false positives
        num_bytes = estimated_word_count * num_probes * 3 // 2 // 8
        wordlist = (w.strip() for f in wordlistfiles for w in open(f))
        BloomFilter.__init__(self, num_bytes, num_probes, wordlist)

    def find_misspellings(self, text):
        return [word for word in text.lower().split() if word not in self]


## Example of subclassing with faster probe functions ################

from hashlib import sha224, sha256

class BloomFilter_4k(BloomFilter):
    # 4Kb (2**15 bins) 13 probes. Holds 1,700 entries with 1 error per 10,000.

    def __init__(self, iterable=()):
        BloomFilter.__init__(self, 4 * 1024, 13, iterable)

    def get_probes(self, key):
        h = int(sha224(key.encode()).hexdigest(), 16)
        for _ in range(13):
            yield h & 32767     # 2 ** 15 - 1
            h >>= 15

class BloomFilter_32k(BloomFilter):
    # 32kb (2**18 bins), 13 probes. Holds 13,600 entries with 1 error per 10,000.

    def __init__(self, iterable=()):
        BloomFilter.__init__(self, 32 * 1024, 13, iterable)

    def get_probes(self, key):
        h = int(sha256(key.encode()).hexdigest(), 16)
        for _ in range(13):
            yield h & 262143    # 2 ** 18 - 1
            h >>= 18


if __name__ == '__main__':

    ## Compute effectiveness statistics for a 125 byte filter with 50 entries

    from random import sample
    from string import ascii_letters

    states = '''Alabama Alaska Arizona Arkansas California Colorado Connecticut
        Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas
        Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota
        Mississippi Missouri Montana Nebraska Nevada NewHampshire NewJersey
        NewMexico NewYork NorthCarolina NorthDakota Ohio Oklahoma Oregon
        Pennsylvania RhodeIsland SouthCarolina SouthDakota Tennessee Texas Utah
        Vermont Virginia Washington WestVirginia Wisconsin Wyoming'''.split()

    bf = BloomFilter(num_bytes=125, num_probes=14, iterable=states)

    m = sum(state in bf for state in states)
    print('%d true positives and %d false negatives out of %d positive trials'
          % (m, len(states)-m, len(states)))

    trials = 100000
    m = sum(''.join(sample(ascii_letters, 8)) in bf for i in range(trials))
    print('%d true negatives and %d false positives out of %d negative trials'
          % (trials-m, m, trials))

    c = ''.join(format(x, '08b') for x in bf.array)
    print('Bit density:', c.count('1') / float(len(c)))


    ## Demonstrate a simple spell checker using a 125,000 word English wordlist

    from glob import glob
    from pprint import pprint

    # Use the GNU ispell wordlist found at http://bit.ly/english_dictionary
    checker = SpellChecker(glob('/Users/raymondhettinger/dictionary/english.?'))
    pprint(checker.find_misspellings('''
        All the werldz a stage
        And all the mehn and wwomen merrely players
        They have their exits and their entrances
        And one man in his thaim pllays many parts
        His actts being sevven ages
    '''))
