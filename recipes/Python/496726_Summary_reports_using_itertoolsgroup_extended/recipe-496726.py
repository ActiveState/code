from itertools import groupby
from operator import itemgetter

def set_keys(*indices):
    """Returns a function that returns a tuple of key values"""
    def get_keys(seq, indices=indices):
        keys = []
        for i in indices:
            keys.append(seq[i])
        return tuple(keys)
    return get_keys
    

def summary(data, key=itemgetter(0), value=itemgetter(1)):
    """Summarise the supplied data.

       Produce a summary of the data, grouped by the given key (default: the
       first item), and giving totals of the given value (default: the second
       item).

       The key and value arguments should be functions which, given a data
       record, return the relevant value.
    """

    for k, group in groupby(data, key):
        yield (k, sum(value(row) for row in group))

if __name__ == "__main__":
    # Example: given a set of sales data for city within region,
    # produce a sales report by region
    sales = [('Scotland', 'Edinburgh', 'Branch1', 20000),
             ('Scotland', 'Glasgow', 'Branch1', 12500),
             ('Scotland', 'Glasgow', 'Branch2', 12000),
             ('Wales', 'Cardiff', 'Branch1', 29700),
             ('Wales', 'Cardiff', 'Branch2', 30000),
             ('Wales', 'Bangor', 'Branch1', 12800),
             ('England', 'London', 'Branch1', 90000),
             ('England', 'London', 'Branch2', 80000),
             ('England', 'London', 'Branch3', 70000),
             ('England', 'Manchester', 'Branch1', 45600),
             ('England', 'Manchester', 'Branch2', 50000),
             ('England', 'Liverpool', 'Branch1', 29700),
             ('England', 'Liverpool', 'Branch2', 25000)]

    sales.sort()
    for (region, city), total in summary(sales, key=set_keys(0,1), value=itemgetter(3)):
        print "%-10s  %-10s : %8d" % (region, city, total)
