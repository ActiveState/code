## Safely and atomically write to a file  
Originally published: 2015-09-02 17:06:29  
Last updated: 2016-03-23 14:14:26  
Author: Steven D'Aprano  
  
Saving the user's data is risky. If you write to a file directly, and an error occurs during the write, you may corrupt the file and lose the user's data. One approach to prevent this is to write to a temporary file, then only when you know the file has been written successfully, over-write the original. This function returns a context manager which can make this more convenient.

Update: this now uses `os.replace` when available, and hopefully will work better on Windows.