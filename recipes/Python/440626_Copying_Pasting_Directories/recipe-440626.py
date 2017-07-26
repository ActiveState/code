'''cap_module.py

The purpose of this module
is to provide functions
for copying and pasting
directories and files.

This is a level 1 module.'''

#=========================
# Level 1 Functions: Files
#=========================

def copy_file(path):
    '''copy_file(string)

    Import the needed functions.
    Assert that the path is a file.
    Return all file data.'''
    from os.path import basename, isfile
    assert isfile(path)
    return (basename(path), file(path, 'rb', 0).read())

def paste_file(file_object, path):
    '''paste_file(tuple, string)

    Import needed functions.
    Assert that the path is a directory.
    Create all file data.'''
    from os.path import isdir, join
    assert isdir(path)
    file(join(path, file_object[0]), 'wb', 0).write(file_object[1])

#===============================
# Level 2 Functions: Directories
#===============================

def copy_dir(path):
    '''copy_dir(string)

    Import needed functions.
    Assert that path is a directory.
    Setup a storage area.
    Write all data to the storage area.
    Return the storage area.'''
    from os import listdir
    from os.path import basename, isdir, isfile, join
    assert isdir(path)
    dir = (basename(path), list())
    for name in listdir(path):
        next_path = join(path, name)
        if isdir(next_path):
            dir[1].append(copy_dir(next_path))
        elif isfile(next_path):
            dir[1].append(copy_file(next_path))
    return dir

def paste_dir(dir_object, path):
    '''paste_dir(tuple, string)

    Import needed functions.
    Assert that the path is a directory.
    Edit the path and create a directory as needed.
    Create all directories and files as needed.'''
    from os import mkdir
    from os.path import isdir, join
    assert isdir(path)
    if dir_object[0] is not '':
        path = join(path, dir_object[0])
        mkdir(path)
    for object in dir_object[1]:
        if type(object[1]) is list:
            paste_dir(object, path)
        else:
            paste_file(object, path)

#================
# CGI: Print File
#================

if __name__ == '__main__':
    from sys import argv
    print 'Content-type: text/plain'
    print
    print file(argv[0]).read()
