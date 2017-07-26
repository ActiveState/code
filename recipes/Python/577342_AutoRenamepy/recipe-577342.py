import os
import sys

def main():
    program = os.path.abspath(sys.argv[0])
    # Get the current working directory and
    # walk through it and its subdirectories.
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd, False):
        # Rename all of the folders.
        for index, name in enumerate(dirs):
            old_name = os.path.join(root, name)
            new_name = os.path.join(root, str(index))
            rename(old_name, new_name)
        # Rename all of the files.
        for index, name in enumerate(files):
            old_name = os.path.join(root, name)
            if old_name != program:
                name, ext = os.path.splitext(name)
                name_ext = '{}{}'.format(index, ext)
                new_name = os.path.join(root, name_ext)
                rename(old_name, new_name)

def rename(old, new):
    try:
        os.rename(old, new)
    except:
        print('Could not rename:', old)

if __name__ == '__main__':
    main()
