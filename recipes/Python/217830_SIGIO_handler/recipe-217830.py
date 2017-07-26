# this handler manages a chain of registered callback functions. 
class SIGIOHandler:
	def __init__(self):
		self.handlers = []
		self.on()
	
	def on(self):
		signal.signal(signal.SIGIO, self)

	def off(self):
		signal.signal(signal.SIGIO, signal.SIG_DFL)

	def register(self, callback):
		self.handlers.append(callback)
		return len(self.handlers) - 1 # the handle

	def unregister(self, handle=0):
		if self.handlers:
			del self.handlers[handle]

	def __call__(self, sig, frame):
		for h in self.handlers:
			h(frame)


# a singleton instance of the SIGIOHandler. Usually, users of this module only
# have to register a DirectoryNotifier object here. Other objects (Dispatcher
# objects) are registered with the poller (which is already set up to be called
# when SIGIO occurs). But you may add your own hooks to it.
try:
	manager
except NameError:
	manager = SIGIOHandler()
