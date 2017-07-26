import os

class iterdir(object):
    def __init__(self, path, deep=False):
	self._root = path
	self._files = None
	self.deep = deep
    def __iter__(self):
	return self
    def next(self):
	if self._files:
	    join = os.path.join
	    d = self._files.pop()
	    r = join(self._root, d)
	    if self.deep and os.path.isdir(r):
		self._files += [join(d,n) for n in os.listdir(r)]
	elif self._files is None:
	    self._files = os.listdir(self._root)
	if self._files:
	    return self._files[-1]
	else:
	    raise StopIteration
   

# sample:
# 	a deep traversal of directories which starts with a vowel
#
it = iterdir('.')
for x in it:
    p = os.path.basename(x)
    it.deep = p[0].lower() in "aeiou"
    print x
