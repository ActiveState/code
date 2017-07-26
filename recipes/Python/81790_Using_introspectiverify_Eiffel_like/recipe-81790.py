import inspect

def signature(function):
	"""Build a string with source code of the function declaration"""
	desc = inspect.getargspec(function)
	if desc[3]:
		ldefault = len(desc[3])
		default = desc[3]
		sign = ','.join(desc[0][:-ldefault])
	else:
		ldefault = 0
		default=[]
		sign = ','.join(desc[0])	
	for n,v in zip(desc[0][-ldefault:],default):
		sign += ','+n+"="+str(v)	
	if desc[1]:
		sign +=',*'+desc[1]
	if desc[2]:
		sign +=',**'+desc[2]	
	if sign and sign[0]==',': sign = sign[1:]
	return sign

def callsignature(function):
	"""Build a string with source code of the function call"""
	desc = inspect.getargspec(function)
	sign = ','.join(desc[0])
	if desc[1]:
		sign +=',*'+desc[1]
	if desc[2]:
		sign +=',**'+desc[2]	
	if sign and sign[0]==',': sign = sign[1:]
	return sign


def contract(function,before,after):
	"""Create a function wraper wich test Eiffel-like contract
	
	before is a string that contain preconditions separed by ;
	after is a string that contain postconditions 
	"""
	if __debug__:		
		def mk_condition(code,text):
			lc=code.split(';')
			code_ins=''
			for i in lc:
				txt = i.strip()
				if txt : code_ins +='	assert '+ txt + ",'" + txt + "'\n"			
			return code_ins
		
		precondition = mk_condition (before,'precondition')
		postcondition = mk_condition (after, 'postcondition')
		real_function = function
		source = ("def func_contract("+ signature(function) +"):\n" +
				precondition +
			    "	result = undercontract_"+function.func_name+"("+
				callsignature(function)+")\n"+
			   	postcondition+"	return result\n")
			
		exec source
		globals()["undercontract_"+function.func_name]=function
		return func_contract
		
		
	else:
		return function


# contract test case
def foo(x,y,g=2,z=1,*rt):
	return x+y+z*g 

foo = contract(foo,'x>1;0<y<100','result>0')

foo(12,31)

class bar:
	def __init__(self):
		self.x = 0
		self.y = 0
	def instr(self,n):
		self.x = n+1
		return n+self.y
	instr=contract(instr,'n>1;self.y<10','self.y==0')

x=bar()
x.instr(2)	
