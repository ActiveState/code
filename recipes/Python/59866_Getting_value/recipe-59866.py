d = {'key':'value',}

# how you might write a test to pull out 
# the value of key from d
if d.has_key('key'):
  print d['key']
else:
  print 'not found'

# a much simpler syntax
print d.get('key', 'not found')
print d.get('foo', 'not found')
