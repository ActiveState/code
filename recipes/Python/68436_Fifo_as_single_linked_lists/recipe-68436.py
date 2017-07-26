class Fifo:
	def __init__(self):
		self.first=()		
	def append(self,data):
		node = [data,()]
		if self.first:
			self.last[1] = node			
		else:
			self.first = node
		self.last = node		
	def pop(self,n=-1):
		node = self.first
		self.first=node[1]
		return node[0]
		

a=Fifo()
a.append(10)
a.append(20)
print a.pop(0)
print a.pop(0)
a.append(5)
print a.pop(0)
