## Simple telnet session scripting  
Originally published: 2002-09-25 10:10:14  
Last updated: 2002-09-25 19:47:17  
Author: Tim Keating  
  
This is an EXTREMELY simple module for scripting a telnet session. It uses abbreviated versions of the commands exported by telnetlib followed by any necessary arguments.

An example of use would be:

import telnetscript

script = """ru Login:
w %(user)s
ru Password:
w %(pwd)s
w cd ~/interestingDir
w ls -l
ra
w exit
c
"""

user = 'foo'
pwd = 'bar'
conn = telnetscript.telnetscript( 'myserver', vars() )
lines = conn.RunScript( script.split( '\n' ))

This assigns lines the value of the output of "ls" in "~/interestingDir" for user foo on myserver.