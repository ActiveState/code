# The purpose of this code is to replace the implementation of popen2.popen* such
# that you can pass Unicode strings to those functions. The Unicode string will
# be converted to a plain string using the UTF-8 encoding.

# The more interesting point made here is that it is possible, and reasonably easy,
# to change the implementation of a method at runtime

import popen2

# This is the replacement routine. All it does in convert the cmd to UTF-8 and pass it
# to the original method. The original method is saved as a default argument (this
# takes advantage of the fact that default arguments are only evaluated once in
# Python).

def _run_child_withencoding(self, cmd, old_run_child = popen2.Popen3._run_child):
    return old_run_child(self, cmd.encode('utf-8'))

# Replace the _run_child method in the Popen3 class with out new implementation
popen2.Popen3._run_child = _run_child_withencoding

# Note that the technique for changing a an method on an instance, instead of a
# class, is somewhat different because Python differentiates between bound and
# unbound instances. But that's for a different recipe :-)
