# Required module
import os

# Function for getting files from a folder
def fetchFiles(pathToFolder, flag, keyWord):
	'''	fetchFiles() requires three arguments: pathToFolder, flag and keyWord
		
	flag must be 'STARTS_WITH' or 'ENDS_WITH'
	keyWord is a string to search the file's name
	
	Be careful, the keyWord is case sensitive and must be exact
	
	Example: fetchFiles('/Documents/Photos/','ENDS_WITH','.jpg')
		
	returns: _pathToFiles and _fileNames '''
	
	_pathToFiles = []
	_fileNames = []

	for dirPath, dirNames, fileNames in os.walk(pathToFolder):
		if flag == 'ENDS_WITH':
			selectedPath = [os.path.join(dirPath,item) for item in fileNames if item.endswith(keyWord)]
			_pathToFiles.extend(selectedPath)
			
			selectedFile = [item for item in fileNames if item.endswith(keyWord)]
			_fileNames.extend(selectedFile)
			
		elif flag == 'STARTS_WITH':
			selectedPath = [os.path.join(dirPath,item) for item in fileNames if item.startswith(keyWord)]
			_pathToFiles.extend(selectedPath)
			
			selectedFile = [item for item in fileNames if item.startswith(keyWord)]
			_fileNames.extend(selectedFile) 
			    
		else:
			print fetchFiles.__doc__
			break
						
		# Try to remove empty entries if none of the required files are in directory
		try:
			_pathToFiles.remove('')
			_imageFiles.remove('')
		except ValueError:
			pass
			
		# Warn if nothing was found in the given path
		if selectedFile == []: 
			print 'No files with given parameters were found in:\n', dirPath, '\n'
		
	print len(_fileNames), 'files were found is searched folder(s)'
				
	return _pathToFiles, _fileNames
