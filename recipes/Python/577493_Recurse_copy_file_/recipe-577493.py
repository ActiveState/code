import os
import sys
import shutil


__doc__ = """ copy all files from  directory to an destination ,
It recreate directory tree of src to dst and replace or create file in this directory
If you have tree like this
src/A/dir/file
src/B/dir/sdir/file2
src/B/dir/file
and
then after script src dst 
dst/dir/file
dst/dir/sdir/file2 -> this is the B file2 wich is taken"""

def copytree(src, dst):
    
    if os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for name in os.listdir(src):
            copytree(os.path.join(src, name),
                     os.path.join(dst, name))
    else:
        shutil.copyfile(src, dst)

def main(dsrc, ddst):
    for dirname in os.listdir(dsrc):
        tocopy = os.path.join(dsrc, dirname)
        for d in os.listdir(tocopy):
            src = os.path.join(tocopy,d)
            dst = os.path.join(ddst,d)
            if os.path.isdir(src):
                copytree(src, dst)

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    main(src, dst)
    
