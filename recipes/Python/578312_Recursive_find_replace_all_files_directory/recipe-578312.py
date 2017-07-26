import os
import fnmatch
import sys
import shutil
import re

def usage():
    print """
Usage:
    %s <work_dir> <search_regex> <replace_with> <glob_pattern> [backup]
    """ % (os.path.basename(sys.argv[0]))

def find_replace(directory, search_pattern, replacement, glob_pattern, create_backup=False):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, glob_pattern):
            pardir = os.path.normpath(os.path.join(path, '..'))
            pardir = os.path.split(pardir)[-1]
            print '[%s]' % pardir,
            filepath = os.path.join(path, filename)
            #backup orig file
            if create_backup:
                backup_path = filepath + '.bak'
                print 'DBG: creating backup', backup_path
                shutil.copyfile(filepath, backup_path)
                
            with open(filepath) as f:
                data = f.read()
                
            with open(filepath, "w") as f:
                print 'DBG: replacing in file', filepath
                # s = s.replace(search_pattern, replacement)
                data = re.sub(search_pattern, replacement, data)
                f.write(data)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit(-1)
        
    work_dir = sys.argv[1]
    search_regex = sys.argv[2]
    replacement = sys.argv[3]
    glob_pattern = sys.argv[4]
    dobackup = (len(sys.argv) > 4) and sys.argv[5].lower() in ['backup', '-b']
    # findReplace(".", "<span[^>]*>", "<div>", "*.html")
    find_replace(work_dir, search_regex, replacement, glob_pattern, dobackup)
