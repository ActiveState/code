# the standard way
data = { 'red' : 1, 'green' : 2, 'blue' : 3 }

# a cleaner way
def dict(**kwargs): return kwargs

data = dict(red=1, green=2, blue=3)
