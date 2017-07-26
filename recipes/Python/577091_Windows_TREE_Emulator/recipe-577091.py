import sys, os

FILES = False

def main():
    if len(sys.argv) > 2 and sys.argv[2].upper() == '/F':
        global FILES; FILES = True
    try:
        tree(sys.argv[1])
    except:
        print('Usage: {} <directory>'.format(os.path.basename(sys.argv[0])))

def tree(path):
    path = os.path.abspath(path)
    dirs, files = listdir(path)[:2]
    print(path)
    walk(path, dirs, files)
    if not dirs:
        print('No subfolders exist')

def walk(root, dirs, files, prefix=''):
    if FILES and files:
        file_prefix = prefix + ('|' if dirs else ' ') + '   '
        for name in files:
            print(file_prefix + name)
        print(file_prefix)
    dir_prefix, walk_prefix = prefix + '+---', prefix + '|   '
    for pos, neg, name in enumerate2(dirs):
        if neg == -1:
            dir_prefix, walk_prefix = prefix + '\\---', prefix + '    '
        print(dir_prefix + name)
        path = os.path.join(root, name)
        try:
            dirs, files = listdir(path)[:2]
        except:
            pass
        else:
            walk(path, dirs, files, walk_prefix)

def listdir(path):
    dirs, files, links = [], [], []
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            dirs.append(name)
        elif os.path.isfile(path_name):
            files.append(name)
        elif os.path.islink(path_name):
            links.append(name)
    return dirs, files, links

def enumerate2(sequence):
    length = len(sequence)
    for count, value in enumerate(sequence):
        yield count, count - length, value

if __name__ == '__main__':
    main()
