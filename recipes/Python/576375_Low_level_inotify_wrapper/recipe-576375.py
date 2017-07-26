'''
    Low level inotify wrapper
'''

from os import read, close
from struct import unpack
from fcntl import ioctl
from termios import FIONREAD
from time import sleep
from ctypes import cdll, c_int, POINTER
from errno import errorcode

libc = cdll.LoadLibrary('libc.so.6')
libc.__errno_location.restype = POINTER(c_int)
def geterr(): return errorcode[libc.__errno_location().contents.value]

class Inotify(object):
    def __init__(self):
        self.fd = libc.inotify_init()
        if self.fd == -1:
            print 'inotify INIT err :', geterr()
            raise OSError()
    def read(self):
        size_int = c_int()
        while ioctl(self.fd, FIONREAD, size_int)==-1: sleep(1)
        size = size_int.value
        if not size: return
        data = read(self.fd, size)
        deb = 0
        while deb < size:
            fin = deb+16
            wd, mask, cookie, name_len = unpack('iIII', data[deb:fin])
            deb, fin = fin, fin+name_len
            name = unpack('%ds' % name_len, data[deb:fin])
            name = name[0].rstrip('\0')
            deb = fin
            yield wd, mask, cookie, name
    def add_watch(self, path, mask):
        wd = libc.inotify_add_watch(self.fd, path, mask)
        if wd == -1: print 'inotify ADD err :', geterr()
        return wd
    def rm_watch(self, wd):
        ret = libc.inotify_rm_watch(self.fd, wd)
        if ret == -1: print 'inotify RM err :', geterr()
    def close(self):
        close(self.fd)

FLAGS = {
    'ACCESS'      : 0x00000001, # IN_ACCESS
    'MODIFY'      : 0x00000002, # IN_MODIFY
    'ATTRIB'      : 0x00000004, # IN_ATTRIB
    'WRITE'       : 0x00000008, # IN_CLOSE_WRITE
    'CLOSE'       : 0x00000010, # IN_CLOSE_NOWRITE
    'OPEN'        : 0x00000020, # IN_OPEN
    'MOVED_FROM'  : 0x00000040, # IN_MOVED_FROM
    'MOVED_TO'    : 0x00000080, # IN_MOVED_TO
    'CREATE'      : 0x00000100, # IN_CREATE
    'DELETE'      : 0x00000200, # IN_DELETE
    'DELETE_SELF' : 0x00000400, # IN_DELETE_SELF
    'MOVE_SELF'   : 0x00000800, # IN_MOVE_SELF
    'UNMOUNT'     : 0x00002000, # IN_UNMOUNT
    'Q_OVERFLOW'  : 0x00004000, # IN_Q_OVERFLOW
    'IGNORED'     : 0x00008000, # IN_IGNORED
    'ONLYDIR'     : 0x01000000, # IN_ONLYDIR
    'DONT_FOLLOW' : 0x02000000, # IN_DONT_FOLLOW
    'MASK_ADD'    : 0x20000000, # IN_MASK_ADD
    'ISDIR'       : 0x40000000, # IN_ISDIR
    'ONESHOT'     : 0x80000000, # IN_ONESHOT
}

def mask_str(mask):
    return ' | '.join(name for name, val in FLAGS.items() if val & mask)
