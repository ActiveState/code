'''
seq1.py
Purpose: To act somewhat like the Unix seq command.
Author: Vasudev Ram
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
'''

import sys

def main():
    sa, lsa = sys.argv, len(sys.argv)
    if lsa < 2:
        sys.exit(1)
    try:
        start = 1
        if lsa == 2:
            end = int(sa[1])
        elif lsa == 3:
            start = int(sa[1])
            end = int(sa[2])
        else: # lsa > 3
            sys.exit(1)
    except ValueError as ve:
        sys.exit(1)

    for num in xrange(start, end + 1):
        print num, 
    sys.exit(0)
    
if __name__ == '__main__':
    main()
