import sys
import os
import platform
import sqlite3

locatedb = os.path.join(os.path.expanduser('~'), 'sqlite3-locate.db')
if os.path.exists(locatedb):
    os.remove(locatedb)

def wholepath():
    pathes = []
    if 'Windows' == platform.system():
        for drv in [chr(d) for d in range(ord('A'), ord('Z')+1)]:
            root = drv + r':' + os.sep
            if os.path.exists(root):
                pathes.append(root)
        return pathes
    return [os.sep]

def mktarget(*targets):
    if len(targets) == 0:
        return wholepath()
    return targets

db = sqlite3.connect(locatedb)
db.text_factory=str
cur = db.cursor()
cur.execute('CREATE TABLE locatedb(path TEXT PRIMARY KEY)')

for target in mktarget(*sys.argv[1:]):
    for root, dirs, files in os.walk(target):
        for fn in files:
            cur.execute('INSERT INTO locatedb VALUES(?)', (os.path.join(root, fn),))
db.commit()
