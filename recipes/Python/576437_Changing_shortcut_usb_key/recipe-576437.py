import sys,glob,re
import pythoncom
from win32com.shell import shell
import win32com
import win32com.client
import string
"""
By bussiere bussiere @at gmail.com
thanks to :
http://www.blog.pythonlibrary.org/
http://www.blog.pythonlibrary.org/?p=21
and :
http://codesnippets.joyent.com/tag/python
http://codesnippets.joyent.com/tag/python#post529
"""

__Author__ ="bussiere"
__Email__ = "bussiere @at gmail.com"
__Titre__ = "Changing shortcut on a usb key v2"
__Description__ = "Changing the drive of a list of shortcut automatically must be placed in the shortcut directory on the usb key"
__Discussion__ = "i've made some shortcut on my usb key for  http://www.launchy.net/ launchy and i had always to change them if on one pc the usb drive was i: on an other it was k: it was such a pain each time. Now it change all the shortcut automatically."
__Tags__ ="Usb shortcut windows key raccourcis"


class Win32Shortcut:
    def __init__(self, lnkname):
        self.shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        self.shortcut.QueryInterface(pythoncom.IID_IPersistFile).Load(lnkname)

    def __getattr__(self, name):
        return getattr(self.shortcut, name)


def main():
    
    shell2 = win32com.client.Dispatch('WScript.Shell')
    # here we just get the drive where is the usb key
    drive = sys.path[0][0:2]
    #here we list all the file on the shortcut directory
    files = glob.glob(sys.path[0]+'/*')
    # here we take one file path
    path = glob.glob(sys.path[0])[0]
    #we normalize the path for python
    path = string.replace(path,'\\','\\\\')
    # we prepare a regexp for finding the shortcuts
    p = re.compile('\.lnk')
    
    for file in files :
        # we list all the files and find the shortcuts .lnk
    	if p.search(file) :
            # we get the shortcut 
            s = Win32Shortcut(file)
            #we take the target directory of the shortcut
            itemPath = s.GetPath(0)[0]
            #we normalize the path of the shortcut
            file = string.replace(file,'\\','\\\\')
            # we overwrite the shortcut (same directory, same name).
            shortcut = shell2.CreateShortCut(file)
            #we replace the target path (drive = usb drive, path without the drive = itemPath[2:])
            shortcut.Targetpath =  drive + itemPath[2:]
            #we set the directory drive
            shortcut.WorkingDirectory = path
    		#we save the shortcut
            shortcut.save()



if __name__ == "__main__":
    main()
