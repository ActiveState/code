#!/usr/bin/env python
import os
import os.path
import sys
import stat
import logging

def gen_feedback(data):
    while True:
        for pos in range(len(data)):
            yield data[pos]

def fix_read_only(fname):
    '''Removes read only attribute if file is read only'''
    fileattr = os.stat(fname)[0] 
    if (not fileattr & stat.S_IWRITE):
        logging.info('Fixing read only file: ' + fname)
        os.chmod(fname, stat.S_IWRITE)

def clear_dir(dirname):
    '''Deletes all files in the directory tree and then dirs'''
    for root, dirs, files in os.walk(dirname):
        for i in files:
            tmpname = os.path.join(root,i)
            logging.info('Deleting file: ' + tmpname)
            try:
                fix_read_only(tmpname)
                os.remove(tmpname)
            except Exception as e:
                logging.exception(e)
    for root, dirs, files in os.walk(dirname):
        for j in dirs:
            tmpname = os.path.join(root,j)
            logging.info('Deleting dir: ' + tmpname)
            try:
                fix_read_only(tmpname)
                os.rmdir(tmpname)
            except Exception as e:
                logging.exception(e)
    try:
        fix_read_only(dirname) 
        logging.info('Deleting dir:' + dirname)
        os.rmdir(dirname)
    except Exception as e:
        logging.exception(e)

if __name__ == '__main__':
    sys.stdout.write('SVN Directory Remover\n')
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        basedir = sys.argv[1]
        dirlist = []  
        fb = gen_feedback('\\|/-') 
        for root, dirs, files in os.walk(basedir):    
            for i in dirs:
                sys.stdout.write(next(fb) + '\r') 
                if i == '.svn':
                    tmpname = os.path.join(root,i)
                    logging.info('Found: ' + tmpname)
                    dirlist.append(tmpname)
        
        if len(dirlist):
            for i in dirlist:
                logging.info('Clearing dir:' + i)
                clear_dir(i)
        else:
            sys.stdout.write('No .svn directories found\n')
    else:
        sys.stdout.write('usage: {0} <dirname>\n')
