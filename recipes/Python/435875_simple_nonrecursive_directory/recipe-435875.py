import os, os.path

startDir = "/"

directories = [startDir]
while len(directories)>0:
    directory = directories.pop()
    for name in os.listdir(directory):
        fullpath = os.path.join(directory,name)
        if os.path.isfile(fullpath):
            print fullpath                # That's a file. Do something with it.
        elif os.path.isdir(fullpath):
            directories.append(fullpath)  # It's a directory, store it.
