#!/usr/bin/python

import readline
import shutil
import sys
import os


def main():
    """
    interactive move of a file. Instead of calling mv with two
    arguments, source and destination, call imv with just the source,
    and edit the destination in a GNU readline buffer.

    Once the line editor is started, it is possible to cancel with
    Ctrl-C without harming the filesystem.
    """
    if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        help(main)
        sys.exit(0)
    else:
        for src in sys.argv[1:]:
            if os.path.exists(src):
                def pre_input_hook():
                    readline.insert_text(src)
                    readline.redisplay()
                readline.set_pre_input_hook(pre_input_hook)
                try:
                    dst = raw_input('imv$ ')
                except KeyboardInterrupt:   # die silently if user hits Ctrl-C
                    pass
                else:
                    shutil.move(src, dst)
            else:
                print 'ERROR: %s: no such file or directory' % src
                sys.exit(-1)

if __name__ == "__main__":
    main()
