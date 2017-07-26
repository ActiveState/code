from collections import namedtuple, OrderedDict
from lib import *

def virtual_container(virtual_container, objects_type):
	"""Used to create a virtual object given a the type of container and what it holds.
	The object_type needs to only have normal values."""
	for name in objects_type:
		if name.startswith("__") and name.endswith("__"):
			raise ValueError("Arguments should be not start and end with __")
	
	if issubclass(virtual_container,list):
		def handle_binding(objects_type):
			class my_virtual_container_class:
				"""This singleton class represents the container"""
				def __init__(self):
					"""The attributes for the virtual container"""
					#Define the default values
					__vals__=OrderedDict([(key,None) for key in objects_type])
					#Then function to access them. Note the default parameter for the lambda to
					#enforce early binding
					d={}
					for key in objects_type:
						def func_factory(key):
							"""Function causes early binding for key"""
							def make_attribute(self, items=None):
								"""Called on the attr_cl. This function will return the list for the attribute.
								 As a default, this is [], but a list can also be passed in"""
								if items==None:
									items=[]		
								if self.__vals__[key]==None:
									self.__vals__[key]=items
								else:
									raise RuntimeError("This attribute has been already initialised")	
								return self.__vals__[key]
							return make_attribute
						#Add the function to this class
						d[key]=func_factory(key)
					
					d["__vals__"]=__vals__
					#Construct a named tuple from this
					self.__attr__=type('attr_cl',(), d)()
					
				#Define the operators
				
				def __iter__(self):
					vals=self.__attr__.__vals__
					return zip(*vals.values())
				
				def __contains__(self, x):
					return x in self.__iter__()
				
				def __delitem__(self, i):
					#Handles items and slices
					vals=self.__attr__.__vals__
					for seq in vals.values():
						del seq[i]

				def __getitem__(self, i):
					#Handles items and slices
					vals=self.__attr__.__vals__
					#Make it a slice
					isslice=isinstance(i, slice)
					if not isslice:
						i=slice(i, i+1)
					ret=[seq[i] for seq in vals.values()]
					ret=list(zip(*ret))
					if not isslice:
						ret=ret[0]
					return ret
				
				def __setitem__(self, i, x):
					#Handles items and slices
					vals=self.__attr__.__vals__
					#Split slices
					if isinstance(i,slice):
						x=zip(*x)
					for seq, setTo in zip(vals.values(), x):
						seq[i]=setTo
				
				def __add__(self, myList):
					return list(self.__iter__())+myList
				
				def __iadd__(self, myList):
					vals=self.__attr__.__vals__
					for seq, extra in zip(vals.values(), zip(*myList)):
						seq+=extra
					return self	
				
				def __str__(self):
					s="Proxy: Names: "+" ".join(self.__attr__.__vals__.keys())
					s+=" Vals: "+" ".join(map(str,self.__iter__()))
					return s
							
			return my_virtual_container_class()
		return handle_binding(objects_type)
	

#Example code
coordinates_2d=["x","y"]
coordinates=virtual_container(list, coordinates_2d)
x=coordinates.__attr__.x([1,2,3,4])
y=coordinates.__attr__.y([2,3,4,5])

print(coordinates[3])
print(coordinates[3:4])
print(coordinates[2:4])
for m in coordinates:
	print(m, end=" ")
print()
print(coordinates+[1,2])
coordinates[1]=(0,0)
print(x,y)
coordinates+=[(9,9)]
print("##",coordinates[:])
del coordinates[1:3]
print(coordinates[:])
coordinates[0:2]=[(0,1),(3,4)]
print(coordinates)

#Testing second group of coordinates
coordinates2=virtual_container(list, coordinates_2d)
x2=coordinates2.__attr__.x([])
y2=coordinates2.__attr__.y([])

print("List is: ", end=" ")
for z in coordinates2:
	print(z,end=" ")
print()
print(bool(coordinates2))
print(coordinates[0])
