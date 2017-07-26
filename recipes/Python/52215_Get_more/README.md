## Get more information from tracebacksOriginally published: 2001-03-07 10:07:34 
Last updated: 2001-03-07 10:07:34 
Author: Bryn Keller 
 
The standard Python traceback module provides very useful functions to produce useful information about where and why an error occurred. Traceback objects actually contain a great deal more information than the traceback module displays, however. That information can greatly assist in detecting the cause of your error.\n\nHere's an example of an extended traceback printer you might use, followed by a usage example.