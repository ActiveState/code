import os
import sys

# NOTE
# ====
# Renaming should happen in groups based on extention.
# All files should first be renamed with a unique ID.

################################################################################

ERR = False
ALL = ''.join(map(chr, xrange(256)))
NUM = '0123456789'
LET = ALL.translate(ALL, NUM)
EXT = 'avi', 'bmp', 'gif', 'jpg', 'wmv'

################################################################################

class Filename:

    def __init__(self, filename):
        self.filename = filename.lower()
        split = self.filename.rsplit('.', 1)
        self.name = split[0]
        self.ext = split[1] if len(split) == 2 else ''
        self.let = self.name.translate(ALL, NUM)
        self.num = self.name.translate(ALL, LET)

    def __eq__(self, other):
        return bool(self.num) and other == int(self.num)

################################################################################

def main():
    try:
        arguments = sys.argv[1:]
        assert arguments
        for path in arguments:
            assert os.path.isdir(path)
        for path in arguments:
            engine(path)
    except:
        sys.stdout.write('Usage: %s <directory>' % os.path.basename(sys.argv[0]))

def engine(path):
    global ERR
    for root, dirs, files in os.walk(path):
        # gather all relevant names
        files = filter(lambda name: name.num and name.ext in EXT, map(Filename, files))
        # find all taken number names
        taken = []
        for name in files[:]:
            if name.name == name.num:
                files.remove(name)
                taken.append(name)
        # put all names in order
        files.sort(compare)
        taken.sort(compare)
        # rename all non-number names
        count = 0
        for name in files:
            while count in taken:
                taken.remove(count)
                count += 1
            name.new = str(count)
            count += 1
        # condense all numerical names
        for name in taken:
            if name.num != str(count):
                name.new = str(count)
                files.append(name)
            count += 1
        # rename files needing new names
        for name in files:
            old = os.path.join(root, name.filename)
            try:
                os.rename(old, os.path.join(root, name.new + '.' + name.ext))
            except:
                sys.stderr.write('%sError: %s' % (ERR and '\n' or '', old))
                ERR = True

def compare(x, y):
    integer = cmp(x.let, y.let)
    return integer if integer else cmp(int(x.num), int(y.num))

################################################################################
    
if __name__ == '__main__':
    main()
