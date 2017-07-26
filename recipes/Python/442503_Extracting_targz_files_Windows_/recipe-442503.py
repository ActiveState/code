import os, sys, tarfile

try:
    tar = tarfile.open(sys.argv[1] + '.tar.gz', 'r:gz')
    for item in tar:
        tar.extract(item)
    print 'Done.'
except:
    name = os.path.basename(sys.argv[0])
    print name[:name.rfind('.')], '<filename>'
