import os, sys

def purge(path):
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        try:
            if os.path.isdir(path_name):
                purge(path_name)
            elif os.path.isfile(path_name):
                size = os.path.getsize(path_name)
                file(path_name, 'wb', 0).write(chr(0) * size)
        except:
            print 'ERROR:', path_name

def main():
    try:
        path = ''
        for index in range(1, len(sys.argv)):
            path += sys.argv[index] + ' '
        path = path[:-1]
        assert os.path.isdir(path)
        purge(path)
        print 'Done.'
    except:
        path = os.path.basename(sys.argv[0])
        path = path[:path.rfind('.')]
        print path, '<directory>'

if __name__ == '__main__':
    main()
