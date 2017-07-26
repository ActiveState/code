d = {}

# To add a key->value pair, do this:
d.setdefault(key, []).append(value)

# To retrieve a list of the values for a key
list_of_values = d[key]

# To remove a key->value pair is still easy, if
# you don't mind leaving empty lists behind when
# the last value for a given key is removed:
d[key].remove(value)

# Despite the empty lists, it's still possible to 
# test for the existance of values easily:
if d.has_key(key) and d[key]:
    pass # has some values for key
else:
    pass # no values for key


# But be warned... this version allows each value
# to be present multiple times:
example = {}
example.setdefault('a', []).append('apple')
example.setdefault('b', []).append('boots')
example.setdefault('c', []).append('cat')
example.setdefault('a', []).append('ant')
example.setdefault('a', []).append('apple')
# NOTE: now example['a'] == ['apple', 'ant', 'apple']
example['a'].remove('apple')
# NOTE: it's still true that ('apple' in example['a'])
