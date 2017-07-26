def group(iterator, count):
    itr = iter(iterator)
    while True:
        yield tuple([itr.next() for i in range(count)])


>>> group([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
<generator object at 0xb7debcac>
>>> list(_)
[(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]

>>> list(group([0, 1, 2, 3, 4, 5, 6], 2))
[(0, 1), (2, 3), (4, 5)]

>>> dataset = ['Nausori', 5, True, 'Namadi', 10, True, 'Lautoka', 8, False, 'Suva', 3, True]
>>> for place, value, truth in group(dataset, 3):
...   if truth:
...     print '%s: %s' % (place, value)
... 
Nausori: 5
Namadi: 10
Suva: 3
