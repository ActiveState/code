a = ['a1', 'a2', 'a3']
b = ['b1', 'b2']

# will iterate 3 times,
# the last iteration, b will be None
print "Map:"
for x, y in map(None, a, b):
  print x, y

# will iterate 2 times,
# the third value of a will not be used
print "Zip:"
for x, y in zip(a, b):
  print x, y

# will iterate 6 times,
# it will iterate over each b, for each a
# producing a slightly different outpu
print "List:"
for x, y in [(x,y) for x in a for y in b]:
    print x, y
