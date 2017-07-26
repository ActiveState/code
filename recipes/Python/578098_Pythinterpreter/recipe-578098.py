#!/usr/bin/env python

"""
Python interpreter auto-completion, history and colored tracebacks.
Installation:

 $ wget http://code.activestate.com/recipes/578098/download/1/ -O ~/.pythonstart
 $ echo "export PYTHONSTARTUP=~/.pythonstart" >> ~/.bashrc
 $ source ~/.bashrc
"""

# Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
# License: MIT

if not hasattr(__name__, "__file__"):  # interpreter mode

    def autocomplete():
        import atexit
        import os
        import readline
        import rlcompleter

        def save_history():
            readline.set_history_length(10000)
            readline.write_history_file(history_path)

        history_path = os.path.expanduser("~/.pyhistory")
        if os.path.exists(history_path):
            readline.read_history_file(history_path)
        atexit.register(save_history)
        readline.parse_and_bind('tab: complete')

    autocomplete()

    del autocomplete
