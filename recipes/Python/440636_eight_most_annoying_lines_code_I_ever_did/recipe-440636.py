old = '-1.py'
import os
os.remove(old)
data = 'old = \'' + str(int(old[:-3]) + 1) + '.py\'\n'
for line in file(str(int(old[:-3]) + 1) + '.py').readlines()[1:]:
    data += line
file(str(int(old[:-3]) + 2) + '.py', 'w').write(data)
os.startfile(str(int(old[:-3]) + 2) + '.py')
