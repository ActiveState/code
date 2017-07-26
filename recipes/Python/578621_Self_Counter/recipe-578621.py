import os, sys
this = int(os.path.splitext(os.path.basename(sys.argv[0]))[0])
os.rename(str(this) + '.py', str(this + 1) + '.py')
os.startfile(str(this + 1) + '.py')
