################################################################
# DirectoryNotifier encapslates the code required for watching directory entry
# contents. Subclass this and override the entry_added() and entry_removed()
# methods. then, instantiate it with a directory name, and register it with the
# sighandler instance.  NOTE: this only works with Python 2.2 or greater on Linux. 
# Example:
#	dn = DirectoryNotifier(os.environ["HOME"])
#	manager.register(dn)

class DirectoryNotifier:
	def __init__(self, dirname):
		if not os.path.isdir(dirname):
			raise RuntimeError, "you can only watch a directory."
		self.dirname = dirname
		self.fd = os.open(dirname, 0)
		self.currentcontents = os.listdir(dirname)
		self.oldsig = fcntl.fcntl(self.fd, fcntl.F_GETSIG)
		fcntl.fcntl(self.fd, fcntl.F_SETSIG, 0)
		fcntl.fcntl(self.fd, fcntl.F_NOTIFY, fcntl.DN_DELETE|fcntl.DN_CREATE|fcntl.DN_MULTISHOT)

	def __del__(self):
#		fcntl.fcntl(self.fd, fcntl.F_SETSIG, self.oldsig)
		os.close(self.fd)
	
	def __str__(self):
		return "%s watching %s" % (self.__class__.__name__, self.dirname)

	# there are lots of race conditions here, but we'll live with that for now.
	def __call__(self, frame):
		newcontents = os.listdir(self.dirname)
		if len(newcontents) > len(self.currentcontents):
			new = filter(lambda item: item not in self.currentcontents, newcontents)
			self.entry_added(new)
		elif len(newcontents) < len(self.currentcontents):
			rem = filter(lambda item: item not in newcontents, self.currentcontents)
			self.entry_removed(rem)
		else:
			self.no_change()
		self.currentcontents = newcontents

	# override these in a subclass
	def entry_added(self, added):
		print added, "added to", self.dirname

	def entry_removed(self, removed):
		print removed, "removed from", self.dirname

	def no_change(self):
		print "No change in", self.dirname
