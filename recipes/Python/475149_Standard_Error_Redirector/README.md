## Standard Error Redirector 
Originally published: 2006-03-18 11:24:08 
Last updated: 2006-03-20 01:53:49 
Author: Stephen Chappell 
 
This recipe was designed for remotely receiving bug reports. It was written after participating in a programming contest where feedback was not helpful. The concept presented here is a step towards working with Python remotely. As sys.stderr is replaced in this recipe, so sys.stdin and sys.stdout can also be redirect to an alternate source (such as sockets connected to another computer).