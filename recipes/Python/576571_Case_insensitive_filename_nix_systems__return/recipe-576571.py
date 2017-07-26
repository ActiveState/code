def getCaseInsensitivePath(path, RET_FOUND=False):
	'''
	Get a case insensitive path on a case sensitive system
	
	RET_FOUND is for internal use only, to avoid too many calls to os.path.exists
	# Example usage
	getCaseInsensitivePath('/hOmE/mE/sOmEpAtH.tXt')
	'''
	import os
	
	if path=='' or os.path.exists(path):
		if RET_FOUND:	ret = path, True
		else:			ret = path
		return ret
	
	f = os.path.basename(path) # f may be a directory or a file
	d = os.path.dirname(path)
	
	suffix = ''
	if not f: # dir ends with a slash?
		if len(d) < len(path):
			suffix = path[:len(path)-len(d)]

		f = os.path.basename(d)
		d = os.path.dirname(d)
	
	if not os.path.exists(d):
		d, found = getCaseInsensitivePath(d, True)
		
		if not found:
			if RET_FOUND:	ret = path, False
			else:			ret = path
			return ret
	
	# at this point, the directory exists but not the file
	
	try: # we are expecting 'd' to be a directory, but it could be a file
		files = os.listdir(d)
	except:
		if RET_FOUND:	ret = path, False
		else:			ret = path
		return ret
	
	f_low = f.lower()
	
	try:	f_nocase = [fl for fl in files if fl.lower() == f_low][0]
	except:	f_nocase = None
	
	if f_nocase:
		if RET_FOUND:	ret = os.path.join(d, f_nocase) + suffix, True
		else:			ret = os.path.join(d, f_nocase) + suffix
		return ret
	else:
		if RET_FOUND:	ret = path, False
		else:			ret = path
		return ret # cant find the right one, just return the path as is.
