'''
tp.py
Purpose: A simple text pager.
Version: 0.1
Platform: Windows-only.
Can be adapted for Unix using tty / termios calls.
Only the use of msvcrt.getch() needs to be changed.
Author: Vasudev Ram
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
'''

import sys
import string
from msvcrt import getch

def pager(in_fil=sys.stdin, lines_per_page=10, quit_key='q'):
    assert lines_per_page > 1 and lines_per_page == int(lines_per_page)
    assert len(quit_key) == 1 and \
        quit_key in (string.ascii_letters + string.digits)
    lin_ctr = 0
    for lin in in_fil:
        sys.stdout.write(lin)
        lin_ctr += 1
        if lin_ctr >= lines_per_page:
            c = getch().lower()
            if c == quit_key.lower():
                break
            else:
                lin_ctr = 0

def main():
    try:
        sa, lsa = sys.argv, len(sys.argv)
        if lsa == 1:
            pager()
        elif lsa == 2:
            with open(sa[1], "r") as in_fil:
                pager(in_fil)
        else:
            sys.stderr.write
            ("Only one input file allowed in this version")
                    
    except IOError as ioe:
        sys.stderr.write("Caught IOError: {}".format(repr(ioe)))
        sys.exit(1)

    except Exception as e:
        sys.stderr.write("Caught Exception: {}".format(repr(e)))
        sys.exit(1)

if __name__ == '__main__':
    main()
