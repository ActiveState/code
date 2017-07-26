## Simple file-based mutex for very basic IPC  
Originally published: 2007-05-09 03:03:48  
Last updated: 2007-05-09 03:03:48  
Author: Vinay Sajip  
  
Since the year dot, file locking has been used as a very simple synchronizing primitive between processes. Here's my take on the approach. To try it, simply start two command windows/terminal windows and run the script in each.\n\nTested on WinXP and Ubuntu (Dapper and Feisty).