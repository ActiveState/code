class MutableInstance(dict):
 def __init__(self):
  self.__dict__ = self

# This makes common tasks easier, not by much but conceptually it unifies things

Foo = MutableInstance()
Foo.x = 5
assert Foo['x'] == 5
Foo.y = 7
assert Foo.keys() == ['x', 'y']
assert Foo.values() == [5, 7]

# And now you can pass it to anything that wants a dictionary too.
