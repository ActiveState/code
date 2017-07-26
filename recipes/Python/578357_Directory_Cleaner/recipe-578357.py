import os, sys

def main(path=''):
    if len(sys.argv) == 1 and path:
        try:
            delete(path)
        except:
            print 'ERROR: Internal Path'
    else:
        try:
            delete(' '.join(sys.argv[1:]))
        except:
            print os.path.basename(sys.argv[0]), '<directory>'

def delete(path):
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        try:
            if os.path.isdir(path_name):
                delete(path_name)
                os.rmdir(path_name)
            elif os.path.isfile(path_name):
                os.remove(path_name)
        except:
            print 'ERROR:', path_name

if __name__ == '__main__':
    main(r'C:\Documents and Settings\SCHAP472')
