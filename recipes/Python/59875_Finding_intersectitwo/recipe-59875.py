# two dictionaries
# blow this up to 1000 to see the difference
some_dict = { 'zope':'zzz', 'python':'rocks' }
another_dict = { 'python':'rocks', 'perl':'$' }

# bad way
# two lots of "in"
intersect = []
for item in some_dict.keys():
  if item in another_dict.keys():
    intersect.append(item)

print "Intersects:", intersect

# good way
# use simple lookup with has_keys()
intersect = []
for item in some_dict.keys():
  if another_dict.has_key(item):
    intersect.append(item)

print "Intersects:", intersect
