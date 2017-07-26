## sane tab completion in pdbOriginally published: 2006-10-07 16:22:00 
Last updated: 2009-07-06 04:35:33 
Author: Stephen Emslie 
 
I make frequent use of python's built-in debugger, but one obvious feature seems to be missing - the bash-like tab completion that you can add to the interpreter. Fortunately pdb's interactive prompt is an instance of Cmd, so we can write our own completion function.\n\nNote: this uses rlcompleter, which isn't available on windows\n\nEdit (6 Jul 2009): import rlcompleter early and force output to stdout to ensure monkeypatch sticks\nEdit: updated to handle changes in local scope\nEdit: Fixed start via 'python -m pdb ...'. Check the comments for details.