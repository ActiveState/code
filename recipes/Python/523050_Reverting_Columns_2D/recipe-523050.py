# the idiom:

def theIdiom(a2Diterable): 
  return zip(*reversed(zip(*a2Diterable))) 

# sample use case:

def invertedDict(aDict):
  return dict(zip(*reversed(zip(*aDict.items()))))
