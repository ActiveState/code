import os
import sys

__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577281-xnview-backup-files-remove-utility/'

root_dn = sys.argv[1]

delete_files = list()

for root, dirs, files in os.walk(root_dn):
    for f in files:
        ii = f.split('.')
        if len(ii) > 2:
            prev_part = ii[-2].lower()
            last_part = ii[-1].lower()
            if last_part in ['jpg', 'jpeg'] and prev_part == 'xnbak':
                ii.pop(-2)
                rotated_name = '.'.join(ii)
                rotated_path = os.path.join(root, rotated_name)
                if os.path.isfile(rotated_path):
                    f_path = os.path.join(root, f)
                    # delete bak file
                    delete_files.append(f_path)

for f_path in delete_files:
    try:
        print f_path
        os.unlink(f_path)
    except OSError:
        print >>sys.stderr, 'ERROR DELETE: %s' % f_path
