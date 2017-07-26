#a script that locks a certain file - it doesn't check (currently)
#the lockfile relevance, lockfiles are now implementd as file_naem.lock
from random import random
from time import sleep
from os import remove
from os.path import exists,dirname,join,isdir
lock_ext='.lock'
timeout = 10
class deadlockError(Exception):
    def __init__(s,filename,lockfile_ext,trieddir,time):
        s.file = filename
        s.lockfile_ext = lockfile_ext
        s.isdir = trieddir
        s.secs = time
    def __str__(s):
        if s.isdir:
            final = join(s.file,s.lockfile_ext)
        else: final = s.file+s.lockfile_ext
        print "couldn't find '"+final+"' for "+s.secs+" seconds, params: "\
              +str((s.file,s.lockfile_ext,s.isdir,s.secs))

def lockfile(file,content=None,lockfile_ext=lock_ext,deadlock_timeout=timeout):
    deadlock = 0.0
    lockfile = file+lockfile_ext
    while (exists(lockfile) or exists(join(dirname(file),lockfile_ext))):
        t = random()/10
        sleep(t)
        deadlock += t
        if deadlock>deadlock_timeout: raise deadlockError(file,lockfile_ext,False,deadlock)
    f = open(lockfile,'w')
    if content!=None: f.write(content)
    f.close()
def releasefile(file,lockfile_ext='.lock'):
    remove(file+lockfile_ext)
    
def lockdir(dir,content=None,lockfile_ext=lock_ext,deadlock_timeout=timeout):
    deadlock = 0.0
    lockfile = join(dir,lockfile_ext)
    while (exists(lockfile)):
        t = random()/10
        sleep(t)
        deadlock+=t
        if deadlock>deadlock_timeout: raise deadlockError(dir,lockfile_ext,True,deadlock)
    f = open(lockfile,'w')
    if content!=None: f.write(content)
    f.close()
def releasedir(dir,lockfile_ext=lock_ext):
    remove(join(dir,lockfile_ext))

def islocked(file,lockfile_ext=lock_ext):
    if isdir(file): return exists(join(file,lockfile_ext))
    return exists(file+lockfile_ext) or exists(join(dirname(file),lockfile_ext))
def lock(file,content=None,lockfile_ext=lock_ext,deadlock_timeout=timeout):
    if isdir(file): lockdir(file,content,lockfile_ext,deadlock_timeout)
    else: lockfile(file,content,lockfile_ext,deadlock_timeout)
def release(file,lockfile_ext=lock_ext):
    if isdir(file): releasedir(file,lockfile_ext)
    else: releasefile(file,lockfile_ext)
"""
lock(r'c:\try.exe')
print islocked(r'c:\try.exe')
release(r'c:\try.exe')
print islocked(r'c:\try.exe')
lock('c:\\')
print islocked('c:\\')
release('c:\\')
print islocked('c:\\')
"""
