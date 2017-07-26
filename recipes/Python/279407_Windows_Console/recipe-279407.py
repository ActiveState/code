# Idea borrowed from Brian Akey - www.ironkeytech.com/pyshell
# Adapted for Windoze by Fuzzyman
# April 2004

# http://www.voidspace.org.uk/atlantibots/pythonutils.html


import os, sys, os.path
import traceback
from StringIO import StringIO
from traceback import print_exc

def findlocals(line):
    """If a local variable is to be referenced with a system command the variable will be escaped with a $.
    This function replaces the variable with it's value.
    The $ character can be escaped anywhere with a \ that will be removed.
    (a literal '\$' then becomes '\\$')
    """
    lpos = line.find(' ')
    if lpos == -1: return line      # if there's no space (no command) then it's not a variable name
    command = line[:lpos]
    params = line[lpos:].strip()
    escapelist = ['$']          # currently just the $ character
    variable = ''
    varon = 0
    newparams = ''
    skip = 0
    params += ' '        # so that a variable at the end of a line is terminated
    for char in params:
        if skip:                    # was the last characetr a '\'
            if char in escapelist:  # if the '\' is followed by a '$' it's not a variable - so jsut move on
                newparams += char
            else:
                newparams += '\\' + char
            skip = 0
            continue
            
        if char == '\\':        # is this an escape character ?
            skip = 1
            continue
        if varon:                           # are we in the process of replacing a variable name
            if char == ' ' or char == '\"': # is this the end of the name ?
                if globals().has_key(variable):
                    newparams += str(globals()[variable]) + ' '              # str or repr ??
                else:
                    print 'No such variable as ' + variable
                    return
                varon = 0
                variable = ''
            else:
                variable += char
            continue
        if char == '$':     # have we found the start of a variable name ?
            varon = 1
            continue
        newparams += char
    newline = command + ' ' + newparams     # rebuild the command line
    return  newline

def chdir(l1):
    """A simple function to change the directory.
    Including handling spaces, quotes etc."""
    l2 = l1
    if l1[0] == '\"'  == l1[-1]: l2 = l1[1:-1]
    if os.path.isdir(l2):
        os.chdir(l2)
    elif os.path.isdir(l2.strip()):
        os.chdir(l2.strip())
    else:
        print 'The system can\'t see directory ' + l1



hist = []
l1 = ''
pt = ' >>> '
quitcom = ['exit', 'x', 'q', 'quit']
credits = """Pyshell for windoze by Fuzzyman.
See http://www.voidspace.org.uk/atlantibots/pythonutils.html"""

print "Welcome to Pyshell for Windoze."
while l1 not in quitcom:   
    try :
        l1 = raw_input(os.getcwd() + pt)
        l1 = l1.strip()                             # note - we lose indentation here... bad if we want to implement functions etc...
        if l1.find('$') != -1:
            l1 = findlocals(l1)       # put in any variables
        if not l1: continue   
        l1 = l1.strip()                            # same here
        hist += [l1]
        if l1[0] == '!':
            os.system(l1[1:])
        elif l1 == 'ls':
            os.system('dir')
        elif l1 == '?':
            print credits
        elif l1.startswith('ls '):
            os.system('dir ' + l1[3:])
        elif l1.startswith('dir ') or l1 == 'dir':
            os.system(l1)
        elif l1.startswith('echo '):
            os.system(l1)
        elif l1 == 'hist':
            del hist[len(hist)-1]
            for h1 in hist:
                print h1
        elif l1.startswith('cd '):
            l1 = l1[3:]
            chdir(l1)
        elif l1[0] == '/' or l1[0] == '\\':
            chdir(l1[1:])
        elif l1 == '..':
            os.chdir(l1)

        else:
            try:
                exec(l1)
            except:
                os.system(l1)
    except (KeyboardInterrupt, EOFError) :                ## ctrl-z or ctrl-c hit
        break
                
    except Exception, e:
        f = StringIO()
        print_exc(file=f)
        a = f.getvalue().splitlines()
        for line in a:
            print line 

    
"""
USAGE

For use on windows systems.
Double click shell.py and it will bring up a console window.

Any of the following commands to exit - 'exit', 'x', 'q', 'quit', ctr-c

'?' brings up a simple credits line.

You can define python variables or expressions - not currently functions - in the usual way.
You can enter system commands in the ususal way.

The command line is first tried as a python command,
if it raises an excpetion it is then tried as a system command.

Single line loops are possible
e.g.
F:\Python Projects\shell >>> for value in [1,2,3,4,5] : print value
1
2
3
4
5
F:\Python Projects\shell >>>

You can insert a python variable (or the string representation of any python object)
into a system command by using $name.

e.g.
F:\Python Projects\shell >>> ls
 Volume in drive F is Other Drive
 Volume Serial Number is 2446-9C27

 Directory of F:\Python Projects\shell

22/04/2004  23:41    <DIR>          .
22/04/2004  23:41    <DIR>          ..
22/04/2004  23:41                42 filelist.txt
21/04/2004  19:52    <DIR>          modules
21/04/2004  20:01             4,450 newshell.py
21/04/2004  14:57             3,347 shell.py
21/04/2004  14:27               109 TODO.txt
               4 File(s)          7,948 bytes
               3 Dir(s)  116,625,092,608 bytes free
F:\Python Projects\shell >>> source  = open('filelist.txt', 'r').readlines()
F:\Python Projects\shell >>> for file in source:print file.strip()
TODO1.txt
TODO2.txt
TODO3.txt
TODO4.txt
F:\Python Projects\shell >>> filename = source[0].strip()
F:\Python Projects\shell >>> echo $filename
 TODO1.txt
F:\Python Projects\shell >>>


Any exceptions are displayed (but non-fatal).



EXTRA COMMANDS

If a line starts with a '!' it is always sent to the system. (Useful if a system command clashes with a valid python name).
'ls' is an aliase for 'dir'
lines starting 'echo' are always a system command
'hist' print the current command history
lines starting '/' are passed straight to cd (minus the leading '/')
'..' is an alias for 'cd ..'

Because we are using the os.system command to launch system commands - typing a command like 'help.html' (or any other valid
file) - launches the file with the program the system uses to view that file. In this case it would launch the file 'help.html'
with the system browser.

Can use the import command to run python programs in our namespace.


ISSUES

lowercase - In windoze commands aren't case sensitive - the system commands I've defined are.
No help function
Can't yet put a system command as part of a loop. (or a python function as the parameters to a system command)
No functions, classes or conditionals.
Can only access 'standard' variables through the '$' operator - not lists or dictionaries.

"""
