# Selective cleanup (deletion) of files (based on category and extension)
# For use by a SABnzbd+ external post-processing script

# Version: 1.05
# Date: 2009/07/19
# License: As-is; public domain
# Requirements: Python 3.1, SABnzbd+ 0.4.11

# Description: This script clean's up (deletes) files with specific extensions, e.g. .sfv, .nzb, but only for downloads belonging to a particular category.

# Remarks:
# The cleanup is performed only in the job directory. Its subdirectories, if any, are not affected.
# Extensions are case-insensitive.

# Usage syntax:
# C:\Python31\python.exe selective_cleanup.py job_directory job_category category_specified ext1 ext2 ... extLast

# Usage examples:
# C:\Python31\python.exe "D:\SABnzbd scripts\selective_cleanup.py" %1 %5 movies sfv
# C:\Python31\python.exe "D:\SABnzbd scripts\selective_cleanup.py" %1 %5 "movies (hd)" sfv nzb

# Keywords:
# sabnzbd+, sabnzbd, post-processing, post-processing script,
# delete, deletion, file deletion, extension, file cleanup, cleanup list

import os, sys

# Parse input arguments
job_dir     = sys.argv[1]
job_cat     = sys.argv[2]
cleanup_cat = sys.argv[3]
exts        = sys.argv[4:]

exts = [ext.lower() for ext in exts]

os.chdir(job_dir)

# Selectively delete files
if job_cat == cleanup_cat:
    files = [i for i in os.listdir(job_dir) if os.path.isfile(i)]
    files = [f for f in files if os.path.splitext(f)[1][1:].lower() in exts]
    for f in files:
        os.remove(f)
        print('Deleted {}'.format(f))
