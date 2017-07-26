#!/usr/bin/python


"""

Name:        newSID.py
Author:      Bill Anderson <bill@noreboots.com>
License:     LGPL


This is a nice little means of generating a 
"Session ID" for things like web sessions and the like.

It returns an ID of the format:
  Joe_db2039967237b1b1be33222268408c1a

where "Joe" was the string passed to the function.
"""

import time,whrandom,md5



def getNewSID(tag):
	"""Build a new Session ID"""
	t1 = time.time()
	time.sleep( whrandom.random() )
	t2 = time.time()
	base = md5.new( tag + str(t1 +t2) )
	sid = tag + '_' + base.hexdigest()
	return sid


if __name__ == '__main__':
	print getNewSID('Joe')
