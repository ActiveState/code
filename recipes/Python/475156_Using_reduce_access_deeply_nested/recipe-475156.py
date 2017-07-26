# In your hand you have a dict instance representing the database 'object'
dbo={'m':{'d':{'v':{'version':1}}}}

# You know this thing corresponds to a table whose rows follow some convention
# indicating 'depth', say '__' hapens to be the seperator.

# You wan't to access a particular element, but you know it only by its column
# name 'm__d__v__version'

name='m__d__v__version'

version = reduce(dict.get, name.split('__'), dbo)

assert version == 1

foo = reduce(dict.get, 'm__d__v__foo'.split('__'), dbo)

assert foo == None
