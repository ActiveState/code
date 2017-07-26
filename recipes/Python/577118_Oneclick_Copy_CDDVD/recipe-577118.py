"""
CdCopy: Windows utility for copying contents of a CD/DVD to local hard disk with
most free space to a directory named for full name of CD/DVD.

It would be convenient to drag and drop a CD/DVD icon onto a local hard drive and 
have the Windows GUI create a directory of the same full name as the CD/DVD
then copy CD/DVD contents to that directory. 

Unfortunately Windows does not allow this. 

This small stand-alone utility will extract the name of the CD/DVD, determine
the local hard disk with the most available space, create a directory using the
name of the CD/DVD, then write the CD/DVD contents to that directory.

Usage:

* Copy CdCopy.py to any location on your computer.
* Check that global CD_PATH has the correct drive letter for your system 
  or specify CD/DVD path in the command line.
* Insert CD/DVD that you wish to copy.
* Double-click on CdCopy.py
- Console window will provide feedback on copying progress.
- On completion, press RETURN to exit utility.

Notes:

* Windows only.
* CdCopy does not check that there is enough room on destination to copy CD/DVD.
* CdCopy will also work using the command line:

    CdCopy
    CdCopy [CD/DVD drive path]

"""
__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="2010-03-16"
try:
    import sys
    import os, os.path
    import win32api
    import win32file
    
    CD_PATH = "D:\\" # change as appropriate or pass in by command line arg
    
    def mkdir_path(path):
        if not os.access(path, os.F_OK):
            os.makedirs(path)
            
    def get_volume_paths():
        paths = []
        try:
            drives = win32api.GetLogicalDriveStrings()
            paths = drives.split("\0")
            paths = paths[0:-1] # cut off null string at end
        except Exception, e:
            print "get_volume_paths failed: %s\n" % e
        return paths
    
    def get_free_space(disk):
        free_space = 0
        try:
            free_space_tuple = win32file.GetDiskFreeSpaceEx(disk)
            free_space = free_space_tuple[0]
        except Exception, e:
            pass # ignores failures for inappropriate disks
        return free_space
    
    def get_volume_name(volume_path):
        volume_name = volume_path[0]
        try:
            volume_name = win32api.GetVolumeInformation(volume_path)[0]
        except Exception, e:
            print "get_volume_name failed: %s\n" % e
        return volume_name
    
    def get_volume_with_most_space():
        volume = ""
        free = 0
        volume_paths = get_volume_paths()
        decorated_list = [(get_free_space(path), path) for path in volume_paths]
        if decorated_list:
            decorated_list.sort()
            decorated_list.reverse()
            free, volume = decorated_list[0]
        return volume, free
    
    def copy_cd(cd_path):
        try:
            dest_vol, free_space = get_volume_with_most_space()
            cd_name = get_volume_name(cd_path)
            dest_dir = os.path.join(dest_vol, cd_name) 
            mkdir_path(dest_dir)
            command = "XCOPY %s* \"%s\" /s /i" % (cd_path, dest_dir)
            print command
            os.system(command)
        except Exception, e:
            print "copy_cd failed: %s\n" % e
    
    if __name__ == '__main__':
        print "CdCopy start..."
        if len(sys.argv) > 1:
            cd_path = sys.argv[1]
        else:
            cd_path = CD_PATH
        copy_cd(cd_path)
        print "CdCopy finished."

except Exception, e:
    print "CdCopy failed ... %s" % e
raw_input("Press RETURN...")
