import os, sys

def main(path=''):
    if len(sys.argv) == 1 and path:
        try:
            assert os.path.isdir(path)
            engine(path)
        except:
            print 'ERROR: Internal Path'
    else:
        path = ' '.join(sys.argv[1:])
        try:
            assert os.path.isdir(path)
            engine(path)
        except:
            print os.path.basename(sys.argv[0]), '<directory>'

def engine(path):
    log = open('files.log', 'w')
    for path, dirs, files in os.walk(path):
        log.write('%s\n' % path)
        for name in files:
            log.write('\t%s\n' % name)
        log.write('\n')
    log.close()

if __name__ == '__main__':
    main('C:\\')
