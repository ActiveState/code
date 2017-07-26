class FixedlenList(list):
	'''
subclass from list, providing all features list has
the list size is fixed. overflow items will be discarded
	
	'''
	def __init__(self,l=0):
		super(FixedlenList,self).__init__()
		self.__length__=l #fixed length
		
	def pop(self,index=-1):
		super(FixedlenList, self).pop(index)
	
	def remove(self,item):
		self.__delitem__(item)
		
	def __delitem__(self,item):
		super(FixedlenList, self).__delitem__(item)
		#self.__length__-=1	
		
	def append(self,item):
		if len(self) >= self.__length__:
			super(FixedlenList, self).pop(0)
		super(FixedlenList, self).append(item)		
	
	def extend(self,aList):
		super(FixedlenList, self).extend(aList)
		self.__delslice__(0,len(self)-self.__length__)

	def insert(self):
		pass

##################
# test cases
##################

def test1():	
	l=FixedlenList(5)
	l.append(1)
	l.append(2)
	l.append(3)
	l.append(4)
	l.append(5)
	l.append(6)
	print repr(l)=='[2, 3, 4, 5, 6]'
	
	
def test2():
	l=FixedlenList(2)
	l.extend([11,12,13])
	print repr(l)=='[12, 13]'
