#!/usr/bin/env python

"""
Python script that runs one-liner python scripts similarly to how Perl runs them

portions based on http://code.activestate.com/recipes/437932-pyline-a-grep-like-sed-like-command-line-tool/
(Graham Fawcett, Jacob Oscarson, Mark Eichin)
interface inspired by Perl
"""

"""
Copyright (C) 2010  Drew Gulino

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import re
import getopt
from getopt import GetoptError
import os

def usage(progname):
    print "Usage: " + progname
    version()
    print """
    ./pyliner (options) "script"
    -a enables auto-split of input into the F[] array.
    -F specifies the characters to split on with the -a option (default=" ")
    -p loops over and prints input.
    -n loops over and does not print input.
    -l strips newlines on input, and adds them on output 
    -M lets you specify module imports
    -o print out parsed and indented script on multiple lines
    -e (assumed - does nothing, added for Perl compatibility)
    
    variables:
    F[] = split input
    line = current input line
    NR = current input line number
    
    functions:
    I(x) = function returns F[x] cast to integer
    f(x) = function returns F[x] cast to float
    
    script:
        newlines are specified with ";"
        ":" will start an indent for the following lines
        "?;" will add a newline and dedent the following lines
        "/;" will reset the indent the far left
        "BEGIN:" starts the an initial script not run in the input loop
        "END:" starts part of the script run after the input loop
        "#/" ends both the "BEGIN:" and "END:" portions of the script
    """

#test.txt=
"""
10,test
1,rest
100,test
10,best
1000,we
1,see
"""

"""
cat test.txt | ./pyline.py -F"," -lane 'BEGIN:sum=0#/if i(0) > 90:sum+=i(0)) END:print sum#/'
1100
"""

"""
pyliner:
cat test.txt | ./pyliner.py -F"," -lane 'BEGIN:sum=0#/a=f(0);if a > 90:sum+=a END:print sum/NR#/'
183.333333333

perl:
cat test.txt | perl -F"," -lane 'BEGIN {$sum=0; } ;$sum=$sum+=@F[0] if @F[0]>90;END { print $sum/$.; }'
183.333333333333
"""

def version():
    print "version: 1.0"

write = sys.stdout.write

def indent_script(script_lines):
    #indent lines
    indent = 0
    next_indent = 0
    script = []
    for cmd in script_lines:
        cmd = cmd.strip()
        if cmd[-1]==(":"):
            indent=indent+1
        if cmd[-1]=="?":
            cmd=cmd[0:-1]
            indent=indent-1
        if cmd[-1]=="/":
            cmd=cmd[0:-1]
            indent=0
        cmd=("\t"*next_indent)+cmd
        next_indent = indent
        script.append(cmd)
    script = '\n'.join(script)
    return script

def split_script(cmd):
    #split lines
    cmd = cmd.replace("?;","?\n")
    cmd = cmd.replace("/;","/\n")
    cmd = cmd.replace(";","\n")
    cmd = cmd.replace(":",":\n")
    return cmd

def main(argv, stdout, environ):
    progname = argv[0]
    split_lines=False
    FS = ' '
    print_input = False
    strip_newlines = False
    no_print_input = False
    output_script = False
    F =[]
    
    def I(x): return int(F[x])
    
    def f(x): return float(F[x])
    # parse options for module imports
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'oaplneM:F:')
    except GetoptError:
        print "Invalid Option!"
        usage(progname)
        return
    
    opts = dict(opts)
    if '-M' in opts:
        for imp in opts['-M'].split(','):
            locals()[imp] = __import__(imp.strip())
    if "-a" in opts:
        split_lines = True
    if '-F' in opts:
        FS = opts['-F']
    if "-p" in opts:
        print_input = True
    if "-l" in opts:
        strip_newlines = True
    if "-n" in opts:
        no_print_input = True
    if "-e" in opts:
        pass
    if "-o" in opts:
        output_script = True

    cmd = ' '.join(args)
    if not cmd.strip():
        cmd = 'line'                        # no-op
    
    begin_cmd = ''
    end_cmd = ''
    
    if cmd.find("BEGIN:") >= 0:
        start=cmd.find("BEGIN:")
        end=cmd.find("#/")
        begin_cmd=cmd[start+6:end]
        cmd=cmd[end+2:]
        
    if cmd.find("END:") >= 0:
        start=cmd.find("END:")
        end=cmd.find("#/")
        end_cmd=cmd[start+4:end]
        cmd=cmd[:start]
    
    cmd = split_script(cmd)
    script_lines = cmd.splitlines()
    
    if len(begin_cmd) > 1:
        begin_cmd = split_script(begin_cmd)
        begin_lines = begin_cmd.splitlines()
        begin_script = indent_script(begin_lines)
    
        begin_codeobj = compile(begin_script, 'command', 'exec')
        result =  eval(begin_codeobj, globals(), locals())
        if result is None or result is False:
            result = ''
        elif isinstance(result, list) or isinstance(result, tuple):
            result = ' '.join(map(str, result))
        else:
            result = str(result)
        write(result)
    
    
    if len(end_cmd) > 1:
        end_cmd = split_script(end_cmd)
        end_lines = end_cmd.splitlines()
        end_script = indent_script(end_lines)
        end_codeobj = compile(end_script, 'command', 'exec')
        
    script = indent_script(script_lines)
    
    if output_script == True:
        print "BEGIN:"
        print begin_script 
        print
        print script 
        print
        print "END:"
        print end_script 
        print
    
    #compile script   
    codeobj = compile(script, 'command', 'exec')
    
    if print_input or no_print_input:
        for num, line in enumerate(sys.stdin):
            #line = line[:-1]
            NR = num + 1
            if strip_newlines == True:
                line = line.strip()
            if print_input == True:
                print(line)
            if split_lines == True:
                F = [w for w in line.split(FS) if len(w)]
            result =  eval(codeobj, globals(), locals())
            if result is None or result is False:
                continue
            elif isinstance(result, list) or isinstance(result, tuple):
                result = ' '.join(map(str, result))
            else:
                result = str(result)
            write(result)
            if strip_newlines == True:
               write('\n')
    
    else:
        result =  eval(codeobj, globals(), locals())
        
    if len(end_cmd) > 1:    
        result =  eval(end_codeobj, globals(), locals())
        if result is None or result is False:
            result = ''
        elif isinstance(result, list) or isinstance(result, tuple):
            result = ' '.join(map(str, result))
        else:
            result = str(result)
        write(result)
    
if __name__ == "__main__":
    main(sys.argv, sys.stdout, os.environ)
