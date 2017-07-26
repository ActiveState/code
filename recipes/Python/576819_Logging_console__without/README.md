## Logging to console .. without surprisesOriginally published: 2009-06-22 16:22:06 
Last updated: 2009-06-25 13:12:55 
Author: Sridhar Ratnakumar 
 
``logging.StreamHandler`` is not the best way to log to console .. as it prints everything to ``sys.stderr`` by default. You can configure it to log to ``sys.stdout`` .. but that means even error/exception will be printed to ``sys.stdout``.\n