## Creating a single instance application (Linux version)Originally published: 2008-02-12 10:03:10 
Last updated: 2008-02-12 10:03:10 
Author: Larry Bates 
 
Sometimes it is necessary to ensure that only one instance of application is running. This quite simple solution uses pid file to achieve this, and will run only on Linux platform.  This is a nearly compatible version to the Windows version posted by Dragan Jovelic (I fixed the mispelling of alreadyrunning method).