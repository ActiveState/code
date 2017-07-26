from itertools import count
from collections import defaultdict

def seive():
    table = defaultdict(list)
    for x in count(2):
        facts = table[x]
        if facts:
            del table[x]
            for p in facts:
                table[x+p] = table[x+p] + [p]
        else:
            table[x*x] = [x]
            yield x
