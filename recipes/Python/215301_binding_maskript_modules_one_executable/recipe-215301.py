#!/bin/sh
PYTHON23=$(which python2.3 2>/dev/null)
if [ ! -x "$PYTHON23" ] ; then
    echo "Python-2.3 executable not found - can't continue!"
    exit 1
fi
exec $PYTHON23 - $0 $@ << END_OF_PYTHON_CODE

import sys
sys.path.insert(0, sys.argv[1])
del sys.argv[0:2]
import main
main.main()

END_OF_PYTHON_CODE
