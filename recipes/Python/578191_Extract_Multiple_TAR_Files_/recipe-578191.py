import os
import sys
import tarfile

def main():
    total = untar(sys.argv[1:])
    if total:
        args = total, total > 1 and 's were' or ' was'
        sys.stdout.write('Report: %s file%s untared.' % args)
    else:
        filename = os.path.basename(sys.argv[0])
        sys.stdout.write('Usage: %s <file_or_dir> ...' % filename)

def untar(paths):
    total = 0
    for path in paths:
        if os.path.isdir(path):
            try:
                dir_list = os.listdir(path)
            except:
                pass
            else:
                total += untar(os.path.join(path, new) for new in dir_list)
        elif os.path.isfile(path):
            try:
                tarfile.open(path).extractall(os.path.dirname(path))
            except:
                pass
            else:
                total += 1
    return total

if __name__ == '__main__':
    main()
