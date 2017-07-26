class globaliser:
	def __getattr__(self,name):
		return globals()[name]

	def __setattr__(self,name,value):
		globals()[name]=value


glob = globaliser()

def test1():
	glob.data = 'hello'

def test2():
	print data
	print glob.data

test1()
test2()
