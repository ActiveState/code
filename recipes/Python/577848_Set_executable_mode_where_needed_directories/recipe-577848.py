#!/bin/env python
import os
import sys
import stat
def set_executable(top):
    error_count=0
    def set_exec(name):
        mode = os.stat(name).st_mode
        new_mode = mode
        if new_mode & stat.S_IRUSR:
            new_mode = new_mode | stat.S_IXUSR
        if new_mode & stat.S_IRGRP:
            new_mode = new_mode | stat.S_IXGRP
        if new_mode & stat.S_IROTH:
            new_mode = new_mode | stat.S_IXOTH
        if (mode != new_mode):
            print "Setting exec for '%s' (mode %o => %o)" % (name, mode, new_mode)
            os.chmod(name, new_mode)
    def unset_exec(name):
        mode = os.stat(name).st_mode
        new_mode = mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        if (mode != new_mode):
            print "Unsetting exec for '%s' (mode %o => %o)" % (name, mode, new_mode)
            os.chmod(name, new_mode)
    for root, dirs, files in os.walk(top):
        for name in files:
            complete_name = os.path.join(root, name)
            if os.path.islink(complete_name): continue
            try: 
                f = open(complete_name, 'r')
                header = f.read(4)
                f.close()
                if header[0:2] == '#!' or header[1:4] == 'ELF':
                    set_exec(complete_name)
                else:
                    unset_exec(complete_name)
            except Exception as e:
                print "%s: %s" %  (complete_name, e.__str__())
                error_count += 1
        for name in dirs:
            complete_name = os.path.join(root, name)
            set_exec(complete_name)
    return error_count

if len(sys.argv) >= 2:
    error_count = 0
    for dir in sys.argv[1:]:
        error_count += set_executable(sys.argv[1])
    if error_count > 0:
        print "There were errors"
        sys.exit(1)
else:
    print "Usage\n\t%s <dir1> [dir2|...]\n" % sys.argv[0]
    
