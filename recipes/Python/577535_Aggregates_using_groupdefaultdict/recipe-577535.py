#How to do aggregates using groupby, defaultdict and Counter on flat files
#This Example computes groups for:
#region, count(region), sum(sales), avg(sales), max(sales), min(sales)
#
#By Nestor Nissen

from csv import DictReader
from operator import itemgetter
from itertools import groupby
from collections import defaultdict, Counter

rawdata = '''
Region,City,Sales
Scotland,Edinburgh,20000
Scotland,Glasgow,12500
Wales,Cardiff,29700
Wales,Bangor,12800
England,London,90000
England,Manchester,45600
England,Liverpool,29700
'''.splitlines()[1:]

indata = list(DictReader(rawdata))

print('Using sort and groupby:')
counts = []
sums = []
avgs = []
maxs = []
mins = []
ordered_data = sorted(indata, key=itemgetter('Region'))
for region, group in groupby(ordered_data, key=itemgetter('Region')):
    group_list = list(group)
    count = sum(1 for city in group_list)
    total = sum(int(city['Sales']) for city in group_list)
    maxsale = max(int(city['Sales']) for city in group_list)
    minsale = min(int(city['Sales']) for city in group_list)
    counts.append((region, count))
    sums.append((region, total))
    avgs.append((region, total/count))
    maxs.append((region, maxsale))
    mins.append((region, minsale))
print('count:',counts, '\nsum:',sums, '\navg:',avgs,
      '\nmax:',maxs, '\nmin:',mins, '\n')

print('Using defaultdict:')
dd_counts = defaultdict(int)
dd_sales = defaultdict(int)
dd_maxs = defaultdict(int)
dd_mins = defaultdict(lambda: 9**99)
for row in indata:
    region = row['Region']
    sales = int(row['Sales'])
    dd_counts[region] += 1
    dd_sales[region] += sales
    dd_maxs[region] = max(dd_maxs[region], sales)
    dd_mins[region] = min(dd_mins[region], sales)
counts = list(dd_counts.items())
sums = list(dd_sales.items())
avgs = [(key, dd_sales[key]/count) for key, count in dd_counts.items()]
maxs = list(dd_maxs.items())
mins = list(dd_mins.items())
print('count:',counts, '\nsum:',sums, '\navg:',avgs,
      '\nmax:',maxs, '\nmin:',mins, '\n')

print('Using counter:')
counts = list(Counter(map(itemgetter('Region'), indata)).items())
print('count:',counts)
