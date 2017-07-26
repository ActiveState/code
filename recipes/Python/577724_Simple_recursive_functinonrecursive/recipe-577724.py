import os

def recursive(path):
	"""Move through all files, directories, and subdirectories of a path"""
	yield path
	for name in os.listdir(path):
		fullpath = os.path.join(path, name)
		if os.path.isdir(fullpath):
			for subpath in recursive(fullpath):
				yield subpath
		else:
			yield fullpath


def nonrecursive(path):
	"""Move through all files, directories, and subdirectories of a path"""
	paths = [path]
	while paths:
            dpath = paths.pop(0)
            yield dpath
            for name in os.listdir(dpath):
                    fullpath = os.path.join(path, name)
                    if os.path.isdir(fullpath):
                            paths.append(fullpath)
                    else:
                            yield fullpath
