## Module to allow Asynchronous subprocess use on Windows and Posix platforms  
Originally published: 2005-09-13 12:36:19  
Last updated: 2006-12-01 17:30:02  
Author: Josiah Carlson  
  
The 'subprocess' module in Python 2.4 has made creating and accessing subprocess streams in Python relatively convenient for all supported platforms, but what if you want to interact with the started subprocess?  That is, what if you want to send a command, read the response, and send a new command based on that response?

Now there is a solution.  The included subprocess.Popen subclass adds three new commonly used methods: recv(maxsize=None), recv_err(maxsize=None), and send(input), along with a utility method: send_recv(input='', maxsize=None).

recv() and recv_err() both read at most maxsize bytes from the started subprocess.
send() sends strings to the started subprocess.
send_recv() will send the provided input, and read up to maxsize bytes from both stdout and stderr.

If any of the pipes are closed, the attributes for those pipes will be set to None, and the methods will return None.

v. 1.3 fixed a few bugs relating to *nix support
v. 1.4,5 fixed initialization on all platforms, a few bugs relating to Windows support, added two utility functions, and added an example of how to use this module.
v. 1.6 fixed linux _recv() and test initialization thanks to Yuri Takhteyev at Stanford.
v. 1.7 removed _setup() and __init__() and fixed subprocess unittests thanks to Antonio Valentino.  Added 4th argument 'tr' to recv_some(), which is, approximately, the number of times it will attempt to recieve data.  Added 5th argument 'stderr' to recv_some(), where when true, will recieve from stderr.  Cleaned up some pipe closing.
v. 1.8 Fixed missing self. parameter in non-windows _recv method thanks to comment.
v. 1.9 Fixed fcntl calls for closed handles.