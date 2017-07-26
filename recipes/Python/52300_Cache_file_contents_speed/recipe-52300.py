import string
class FileCache:
	'''Caches the contents of a set of files.
	Avoids reading files repeatedly from disk by holding onto the
	contents of each file as a list of strings.
	'''

	def __init__(self):
		self.filecache = {}
		
	def grabFile(self, filename):
		'''Return the contents of a file as a list of strings.
		New line characters are removed.
		'''
		if not self.filecache.has_key(filename):
			f = open(filename, "r")
			self.filecache[filename] = string.split(f.read(), '\n')
			f.close()
		return self.filecache[filename]
