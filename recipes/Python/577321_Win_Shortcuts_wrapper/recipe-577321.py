from os.path import normpath, exists

import win32com.client

from tools import propertx # from http://code.activestate.com/recipes/502243/

class Link(object):
    def __init__(self, path, target=None):
        path=normpath(path)
        if not path.endswith('.lnk'): path+='.lnk'
        self.path=path
        if target: self.target=target
    @property
    def _link(self):
        shell=win32com.client.Dispatch('WScript.shell')
        return shell.CreateShortCut(self.path)
    @propertx
    def target():
        def set(self, target):
            target=normpath(target)
            if exists(target):
                link=self._link
                link.Targetpath=target
                link.save()
        def get(self):
            if exists(self.path):
                return self._link.Targetpath
        return get, set
    def __str__(self):
        return '%s -> %s' % (self.path[:-4], self.target or '')

if __name__=='__main__':

    # Creates shortcuts in the current directory

    notepad=Link('notepad', 'c:/windows/notepad.exe')
    print notepad
    regedit=Link('regedit')
    print regedit
    regedit.target='c:/windows/regedit.exe'
    print regedit
