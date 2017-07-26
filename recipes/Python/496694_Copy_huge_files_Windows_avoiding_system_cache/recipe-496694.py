import win32file

def copy_big_file(srcname, dstname):
	hin= win32file.CreateFile(
		srcname,
		win32file.GENERIC_READ,
		0, # win32file.FILE_SHARE_READ,
		None,
		win32file.OPEN_EXISTING,
		win32file.FILE_FLAG_SEQUENTIAL_SCAN,
		0)
##	print "type of hin=%r" % type(hin)
	hou= win32file.CreateFile(
		dstname,
		win32file.GENERIC_WRITE,
		0, # win32file.FILE_SHARE_READ,
		None,
		win32file.CREATE_ALWAYS,
		win32file.FILE_FLAG_SEQUENTIAL_SCAN,
		0)
	while 1:
		rc, buffer= win32file.ReadFile(hin, 65536)
		if not buffer: break
		if rc == 0:
			win32file.WriteFile(hou, buffer)
		else:
			print "rc=%d" % rc
			break
	hin.Close()
	hou.Close()
