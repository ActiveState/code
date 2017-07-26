## Fork a daemon process on Unix  
Originally published: 2001-07-10 14:01:38  
Last updated: 2001-07-10 14:01:38  
Author: Jürgen Hermann  
  
Forking a daemon on Unix requires a certain sequence of system calls. Since Python exposes a full POSIX interface, this can be done in Python, too.