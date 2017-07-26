def allindices(string, sub, listindex, offset):
        #call as l = allindices(string, sub, [], 0)
	if (string.find(sub) == -1):
		return listindex
	else:
		offset = string.index(sub)+offset
		listindex.append(offset)
		string = string[(string.index(sub)+1):]
		return allindices(string, sub, listindex, offset+1)
