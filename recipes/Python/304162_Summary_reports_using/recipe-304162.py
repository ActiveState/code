from itertools import groupby
from operator import itemgetter

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
    sales = [('Scotland', 'Edinburgh', 20000),
             ('Scotland', 'Glasgow', 12500),
             ('Wales', 'Cardiff', 29700),
             ('Wales', 'Bangor', 12800),
             ('England', 'London', 90000),
             ('England', 'Manchester', 45600),
             ('England', 'Liverpool', 29700)]

    for region, total in summary(sales, key=itemgetter(0), value=itemgetter(2)):
        print "%10s: %d" % (region, total)
