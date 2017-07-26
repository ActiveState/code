>>> from collections import defaultdict
>>> from itertools import repeat
      
>>> d = defaultdict(repeat('').next)  # default to an empty string
>>> d['abc'] += 'more text'
>>> d['abc']
'more text'


>>> d = defaultdict(repeat('<missing>').next)	# default to 'missing'
>>> d.update(name='John', action='ran')
>>> '%(name)s %(action)s to %(object)s' % d
'John ran to <missing>'


>>> d = defaultdict(repeat(0).next)  # default to zero
>>> for char in 'abracadabra':
	d[char] += 1
>>> d.items()
[('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)]
