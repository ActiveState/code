def loadLibrary(lib,i=0,path=''):
	#Uses: loadLibrary( 'libs.api.VKontakte' )
	
	#print sys.path
	#print 'loadLibrary( lib="'+lib+'", i='+str(i)+', path="'+path+'")'
	
	s = lib.split('.')
	if i == 0:
		for pos in sys.path:
			if os.path.isdir( pos ):
				for p in os.listdir( pos + path ):
					if os.path.isdir( p ):
						if p == s[i]:
							loadLibrary(lib,i=i+1,path=pos+'/'+p)
							break
	else:
		if i < len(s)-1:
			for pos in os.listdir( path ):
				if os.path.isdir( path+'/'+pos ):
					if pos == s[i]:
						loadLibrary(lib,i=i+1,path=path+'/'+pos)
						break
		else:
			possibilities = os.listdir( path )
			for possibility in possibilities:
				#print possibility[0:-3]
				if possibility[0:-3] == s[i]:
					#print 'Yes!'
					fp = file(path + '/' + possibility)
					exec fp in globals()
					fp.close()
