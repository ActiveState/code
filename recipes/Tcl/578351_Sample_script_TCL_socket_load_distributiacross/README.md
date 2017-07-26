## Sample script for TCL socket load distribution across many CPUs / hosts Originally published: 2012-11-29 17:27:19 
Last updated: 2012-11-29 17:27:20 
Author: John Brearley 
 
Here is a demo script for others to reuse / learn from. The server process hands out work assignments to multiple children process to do load balancing across multiple CPUs / hosts. The children process in this sample script dont do any real work, but occasionally create an error to demonstrate the error handling and recovery. Enjoy!