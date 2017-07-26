# save this in .pdbrc in your home directory
import os
import sys
# import rlcompleter early, as it contains side effects
import rlcompleter
# refresh the terminal
os.system("stty sane")
# this rc file takes single lines, so define our complete function here
execfile(os.path.expanduser("~/.pdbrc.py"))
# replace the Pdb class's complete method with ours
sys._getframe(1).f_globals['Pdb'].complete = complete
# set use_rawinput to 1 as tab completion relies on rawinput being used
sys._getframe(1).f_locals['self'].use_rawinput = 1

# save this in .pdbrc.py in your home directory
def complete(self, text, state):
    """return the next possible completion for text, using the current frame's
       local namespace

       This is called successively with state == 0, 1, 2, ... until it
       returns None.  The completion should begin with 'text'.
    """
    # keep a completer class, and make sure that it uses the current local scope 
    if not hasattr(self, 'completer'):
        self.completer = rlcompleter.Completer(self.curframe.f_locals)
    else:
        self.completer.namespace = self.curframe.f_locals
    return self.completer.complete(text, state)
