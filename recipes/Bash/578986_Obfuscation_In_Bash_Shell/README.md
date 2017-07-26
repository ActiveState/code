## Obfuscation In Bash Shell.  
Originally published: 2014-12-19 20:01:29  
Last updated: 2014-12-19 20:01:30  
Author: Barry Walker  
  
IMO, the immense power of the shell...

Please let me know if there is any other human readable language that can do this...

The DEMO code below was an idea I formed to see how to make a bash script very difficult to hack.

Everything in it is made easy to read so as to see this idea working.

It uses bash variables ONLY and although I have used bash loops to create the variables in this
DEMO you could create your own set of variables and 'source' them to the the obfuscated code before
running the main body of the code.

It also goes without saying that you could obfuscate the changing of any or all the variable
allocations at any time AFTER the code runs to make it even more obfuscated and as may times as
you wish...

I would be seriously difficult to actually write a lsrge bash app' using this method but boy oh boy
would it be fun?!?

Testbed:- Macbook Pro, OSX 10.7.x and above, using default bash terminal...

LBNL, yeah I am aware of 'eval' but as it is obfuscated and can have as many obfuscated variables as
I wish allocated to it then why worry... ;o)

Enjoy finding simple solutions to often very difficult problems...

Bazza...