import os
import tarfile

dstfolder = '/somepath/to/output'
fileorfoldertobackup = '/home/username'
dst = '%s.tar.bz2' % os.path.join(dstfolder, os.path.basename(fileorfoldertobackup))
out = tarfile.TarFile.open(dst, 'w:bz2')
out.addfile(fileorfoldertobackup, arcname=os.path.basename(fileorfoldertobackup))
out.close()

You can add as many 'addfile' commands as you would like. I hope this saves someone the momentary confusion I experienced.
