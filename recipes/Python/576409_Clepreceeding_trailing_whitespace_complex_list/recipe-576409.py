import types

def cleanWhiteSpace(obj):
	objType = type(obj)
	if(objType is types.StringType):		# String
		# Clean regular string
		return obj.lstrip().rstrip()
	elif((objType is types.ListType) or (objType is types.TupleType)):		# List or Tuple
		out = [] 
		for ele in obj:		# Iterate the elements
			out.append(cleanWhiteSpace(ele))	# Recurse into this function for the element
		return out
	elif(objType is types.DictType):		# Dictionary 
		out = {}
		for ele in obj:		# Iterate the elements
			out[ele] = cleanWhiteSpace(obj[ele])	# Recurse into this function for the element
		return out
	else:
		# Non String or list object return it
		return obj
