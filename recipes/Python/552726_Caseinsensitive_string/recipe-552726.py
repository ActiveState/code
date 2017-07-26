import re

class str_cir(str):
	''' A string with a built-in case-insensitive replacement method '''
	
	def ireplace(self,old,new,count=0):
		''' Behaves like S.replace(), but does so in a case-insensitive
		fashion. '''
		pattern = re.compile(re.escape(old),re.I)
		return re.sub(pattern,new,self,count)
