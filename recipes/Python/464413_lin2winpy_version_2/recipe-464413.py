import os, sys

def main():
    try:
        search(' '.join(sys.argv[1:]))
        print 'Done.'
    except:
        print os.path.basename(sys.argv[0]), '<directory>'

def search(path):
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            search(path_name)
        elif os.path.isfile(path_name):
            data = file(path_name).read()
            file(path_name, 'w').write(data)

if __name__ == '__main__':
    main()
