## Simple telnet session scripting  
Originally published: 2002-09-25 10:10:14  
Last updated: 2002-09-25 19:47:17  
Author: Tim Keating  
  
This is an EXTREMELY simple module for scripting a telnet session. It uses abbreviated versions of the commands exported by telnetlib followed by any necessary arguments.\n\nAn example of use would be:\n\nimport telnetscript\n\nscript = """ru Login:\nw %(user)s\nru Password:\nw %(pwd)s\nw cd ~/interestingDir\nw ls -l\nra\nw exit\nc\n"""\n\nuser = 'foo'\npwd = 'bar'\nconn = telnetscript.telnetscript( 'myserver', vars() )\nlines = conn.RunScript( script.split( '\\n' ))\n\nThis assigns lines the value of the output of "ls" in "~/interestingDir" for user foo on myserver.