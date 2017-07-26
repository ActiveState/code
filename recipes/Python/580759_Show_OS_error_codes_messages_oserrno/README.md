## Show OS error codes and messages from the os.errno module  
Originally published: 2017-03-01 17:16:45  
Last updated: 2017-03-01 17:18:23  
Author: Vasudev Ram  
  
This recipe is a simple Python introspection utility that displays the defined OS error codes and messages (that Python knows about) from the os.errno module. It works for both Python 2 and Python 3. For each kind of OS error defined in Python, it will display a serial number, the error code, and the corresponding error name, and English error message. E.g. the first few lines of its output are shown below:

$ py -2 os_errno_info.py

Showing error codes and names

from the os.errno module:

Python sys.version: 2.7.12

Number of error codes: 86

 Idx    Code   Name                    Message

   0       1   EPERM                   Operation not permitted

   1       2   ENOENT                  No such file or directory

   2       3   ESRCH                   No such process

   3       4   EINTR                   Interrupted function call

   4       5   EIO                     Input/output error

More information, full output and other details are available here:

https://jugad2.blogspot.in/2017/03/show-error-numbers-and-codes-from.html

