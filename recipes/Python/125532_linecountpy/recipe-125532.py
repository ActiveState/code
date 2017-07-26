 #!/usr/local/bin/python

import re
import os
import sys 
import glob

# regex to handle various comment styles.
expression = re.compile('^\s*?[/*|//|#][*]*.*?')

def parse(sourcefile):
    lcount, ccount = 0, 0

    try:
        file = open(sourcefile, 'r')
    except IOError:
        sys.exit(0)

    for line in file.readlines():
        lcount += 1
        if expression.match(line):
            ccount += 1

    file.close()
    return lcount, ccount


def main():
    # total line count, total comment count
    tlc = tcc = 0    
     
    if not len(sys.argv) > 1:
        print 'Provide filename or extension'
    else:
        for file in glob.glob(sys.argv[1]):
            lc, cc = parse(file)
            print 'processing file: %(file)s %(lc)s' % locals()
            tlc += lc
            tcc += cc
    
    print 'total lines = %(tlc)s\ntotal comments = %(tcc)s' % locals()


if __name__ == "__main__": main()
