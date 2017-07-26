## secondsToStr - h:mm:ss.sss formatting of floating point seconds  
Originally published: 2007-04-20 07:28:47  
Last updated: 2007-04-20 07:28:47  
Author: Paul McGuire  
  
Here is a small footprint routine to convert a number of floating point seconds (such as an elapsed time, found by subtracting an earlier return value from time.time() from a later value) to "0:00:00.000" format, instead of "time.strftime("%H:%M:%S",time.gmtime(t2-t1))+(".%03d" % (((t2-t1)-int(t2-t1))*1000))"