"""
This is a bit of an experiment with a technique of applying filters to lists of
files.

The base functions are IterFiles which is a simple wrapper around os.walk and
then Filter which is used to create filter functions.

Whitelist and Blacklist are then examples of filters created using the Filter 
function as a decorator

As a demonstration of creating filters on the fly, HasMode is then created in 
the __main__ section
"""

import os
import fnmatch
import time

__author__ = 'Eysteinn Kristinsson <eysispeisi@gmail.com>'

def IterFiles(folder, **extraWalkArgs):
    '''
    A simple wrapper around os.walk that returns file paths.
    **extraWalkArgs are passed to os.walk if you want to change the defaults 
    there.
    '''
    for root, dirs, files in os.walk(folder, **extraWalkArgs):
        for fileName in files:
            yield os.path.join(root, fileName)

def Filter(func):
    '''
    This is the filter creator function, you can also use it as a decorator.

    usage: Filter(function, *args **keywordArgs)
    args and keywordArgs are automatically passed to the function during 
    iteration.

    The function passed to it must take a valid file path as a first argument
    example:
        @Filter
        def MinSize(file, minsize):
            return os.path.getsize(file) >= minsize:
        # Now you have created a filter that can take a list of files and a
        # minsize argument and apply the minsize condition to the files list
        # Print files in '.' that are 1MB or larger
        for file in MinSize(os.listdir('.'), 1024*1024):
            print file
    '''
    def wrapper(files, *a, **kw):
        for file in files:
            if func(file, *a, **kw):
                yield file
    return wrapper

@Filter
def Whitelist(file, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(file, pat):
            return True
    return False

@Filter
def Blacklist(file, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(file, pat):
            return False
    return True

if __name__ == '__main__':
    folder = '.' # folder to process

    # get an iterator of all files under <folder>
    files = IterFiles(folder)
    # apply a whitelist to the files iterator
    wfiles = Whitelist(files, ('*.py', '*.txt'))
    # apply a blacklist to the whitelisted-files iterator
    bfiles = Blacklist(wfiles, ('*/__init__.py','*/*test*.py'))
    print 'whitelist/blacklist test'
    print bfiles # prints a generator object as we haven't iterated over it yet
    for file in bfiles: # iterate and print results
        print '  ', file

    # Filters can also constructed on the fly
    # the HasMode function constructed here checks the file mode, it filters
    # out all files that don't have the mode you pass into it.
    import stat # for permission constants
    HasMode = Filter(lambda file, mode: os.stat(file).st_mode & mode == mode)
    print 'files others have read and write access to'
    mode = stat.S_IROTH|stat.S_IWOTH
    for file in HasMode(IterFiles(folder), mode):
        print '  ', file
    print

    # just to state the obvious, you don't have to use IterFilesInFolder to get
    # a list of files to feed a filter, just something that is iterable but 
    # contains actual valid file paths
    files = os.listdir('.')
    print 'python files in current dir'
    for file in Whitelist(files, ('*.py',)):
        print '  ', file
    print
