import os, sys

def file_work(path):
    data = file(path).read()
    os.remove(path)
    file(path, 'w').write(data)

def dir_work(path):
    dirlist = os.listdir(path)
    for name in dirlist:
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            dir_work(full_path)
        elif os.path.isfile(full_path):
            file_work(full_path)

try:
    path = sys.argv[1]
    dir_work(path)
    print 'Done.'
except:
    name = os.path.basename(sys.argv[0])
    print name[:name.rfind('.')], '<directory>'
