# Remove .pyc files from svn from the current directory tree.

import os
import subprocess

# Delete the files first.

for dirpath, dirnames, filenames in os.walk(os.getcwd()):
    for each_file in filenames:
        if each_file.endswith('.pyc'):
            if os.path.exists(os.path.join(dirpath, each_file)):
                os.remove(os.path.join(dirpath, each_file))

# Now, get the svn status and remove the deleted files.

cout, cerr  = subprocess.Popen('svn status .', shell=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE).communicate()
files = cout.split('\n')
output = []

for fname in files:
    if fname.startswith('!'):
        output.append(fname.strip('!').strip())

for each in output:
    try:
        os.system('svn remove ' + each)
    except Exception, e:
        print e
