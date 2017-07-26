import os, shutil, sys

# if not root...kick 
if not os.geteuid()==0:
    sys.exit("\nYou have to be root to access all files\n")

# check if backup dir exist, if not create
if not os.path.isdir("/backup"):
    os.mkdir("/backup", 384) #decimal file permission

# scan entire disk for *.conf* files
for root, dirs, files in os.walk('/'):
    for filename in files:
        if ".conf" in filename:
            abspath = os.path.join(root, filename)
            shutil.copy2(abspath, "/backup") # all your config files are now in /backup
