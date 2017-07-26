import win32con, win32api,os

file='test'
f=open('test','w')
f.close()

#make the file hidden
win32api.SetFileAttributes(file,win32con.FILE_ATTRIBUTE_HIDDEN)

#make the file read only
win32api.SetFileAttributes(file,win32con.FILE_ATTRIBUTE_READONLY)

#to force deletion of a file set it to normal
win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_NORMAL)
os.remove(file) 
