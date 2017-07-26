class SmartDict(dict):

	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError as e:
			raise AttributeError(e)
	def __setattr__(self, name, value):
		self[name] = value
