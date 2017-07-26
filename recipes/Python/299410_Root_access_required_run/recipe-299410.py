import os, sys

# if not root...kick out
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")
