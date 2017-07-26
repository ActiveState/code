#!/usr/bin/env python
import os
import runpy


PKG = 'XXX'  # TODO Change to the name of your package (not your executable!).

try:
    run_globals = runpy.run_module(PKG, run_name='__main__', alter_sys=True)
    executed = os.path.splitext(os.path.basename(run_globals['__file__']))[0]
    if executed != '__main__':  # For Python 2.5 compatibility
        raise ImportError('Incorrectly executed %s instead of __main__' %
                            executed)
except ImportError:  # For Python 2.6 compatibility
    runpy.run_module('%s.__main__' % PKG, run_name='__main__', alter_sys=True)
