# -*- coding: cp1251 -*-
import os, os.path
import sys
import stat
import locale

__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="2010-07-17"

ONE_MEG = 2 ** 20
ONE_GIG = 2 ** 30
DEFAULT_THRESHOLD = 100 * ONE_MEG
DEFAULT_DIR = "c:\\"

class Walker(object):
    def __init__(self, dir):
        self.dir = dir
            
    def is_valid_file(self, file_name):
        return True
        
    def is_valid_dir(self, dir):
        return True
                  
    def execute_file(self, path):
        pass
            
    def execute_dir(self, path):
        pass

    def execute(self):
        for root, dirs, file_names in os.walk(self.dir):
            for file_name in file_names:
                if self.is_valid_dir(root) and self.is_valid_file(file_name):
                    path = os.path.join(root, file_name)
                    self.execute_file(path)
            for dir in dirs:
                if self.is_valid_dir(root):
                    path = os.path.join(root, dir)
                    self.execute_dir(path)
        return self 

class BigDirs(Walker):
    def __init__(self, dir, threshold=DEFAULT_THRESHOLD):
        Walker.__init__(self, dir)
        self.threshold = threshold
        self.dirs = {}

    def execute_file(self, path):
        try:
            file_size = os.path.getsize(path)
            dir, name = os.path.split(path)
            cur_size = self.dirs.get(dir, 0)
            self.dirs[dir] = cur_size + file_size
        except Exception, e:
            sys.stderr.write("%s %s %s\n" % ("BigDirs.execute_file", path, e))
        
    def execute(self):
        try:
            locale.setlocale(locale.LC_ALL, "")
            Walker.execute(self)
            keys = self.dirs.keys()
            decorated_list = [ (self.dirs[key], key) for key in keys ]
            decorated_list.sort()
            for item in decorated_list:
                if item[0] > self.threshold:
                    print "%10s MB %s" % (locale.format('%d', item[0]/ONE_MEG, True), item[1])
        except Exception, e:
            sys.stderr.write("%s %s\n" % ("BigDirs.execute", e))
        return self 

if __name__ == "__main__": 
    walker = BigDirs(DEFAULT_DIR, DEFAULT_THRESHOLD).execute()
    raw_input("BigDirs complete. Press RETURN...")
