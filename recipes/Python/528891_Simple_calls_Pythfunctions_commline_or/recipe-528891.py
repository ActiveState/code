"""
PythonCall.py

PythonCall is a shortcut that allows a CLI command with arguments to call 
any function within a Python module with only two lines of plumbing code.

Usage
=====
* Add code below to bottom of Python module.
    if __name__ == "__main__":
        import sys, PythonCall
        PythonCall.PythonCall(sys.argv).execute()
        
* From command line or desktop shortcut, build a command of form:
    <pythonpath> <module> <function> <arg1 arg2 ...>
    Example: C:\Python25\python.exe C:\Dev\PyUtils\src\TextUtils.py xclip wrap 64
            
Notes
=====
* Called functions must expect args to be strings and do their own conversions.
* No argument checking or error-checking.
* In case of exception, PythonCall sends message to stderr.
* I often use this with text I pass in via the clipboard, which requires
  code to read and write the clipboard (not included here).

Tested with Windows; should work on other platforms.

Jack Trainor 2008
"""
import os, os.path
import sys
import types

class PythonCall(object):
    def __init__(self, sysArgs):
        try:
            self.function = None
            self.args = []
            self.modulePath = sysArgs[0]
            self.moduleDir, tail = os.path.split(self.modulePath)
            self.moduleName, ext = os.path.splitext(tail)
            __import__(self.moduleName)
            self.module = sys.modules[self.moduleName]
            if len(sysArgs) > 1:
                self.functionName = sysArgs[1]
                self.function = self.module.__dict__[self.functionName]
                self.args = sysArgs[2:] 
        except Exception, e:
            sys.stderr.write("%s %s\n" % ("PythonCall#__init__", e))

    def execute(self):
        try:
            if self.function:
                self.function(*self.args)
        except Exception, e:
            sys.stderr.write("%s %s\n" % ("PythonCall#execute", e))
            
            
#####################################################
# Test Examples - REMOVE
#
# Normally the function calls are in a module other than PythonCall. 
# These are only examples.
#
# Example 1: C:\Python25\python.exe C:\Dev\PyUtils\src\PythonCall.py double 14
# Example 2: C:\Python25\python.exe C:\Dev\PyUtils\src\PythonCall.py capitalize "Four score and seven years ago..."
#####################################################

def double(x):
    x = int(x)
    print 2 * x

def capitalize(s):
    print s.upper()

if __name__ == "__main__":
    import sys, PythonCall
    PythonCall.PythonCall(sys.argv).execute()

#####################################################
# End - REMOVE
#####################################################
