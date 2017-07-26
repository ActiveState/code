class passwd(str):
	def __repr__(self):
		return repr('*' * self.__len__())
