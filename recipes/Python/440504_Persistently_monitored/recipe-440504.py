#!/usr/bin/python
import shelve
import time

class collection(object):
	def __init__(self, db):
		self.db = db

	def __call__(self, objects):
		# get the current time in seconds
		now = time.time()

		# create/open the shelve db
		d = shelve.open(self.db, 'c')

		# find & remove the missing items from the collection
		removed = [k for k in d if k not in objects]
		for remove in removed:
			d.pop(remove)

		# find & add new items to the collection
		added = [k for k in objects if k not in d]
		for obj in added:
			d[obj] = now 

		# build a list of tuples (item + age in seconds) 
		items = [(k, int((now - d[k]))) for k in d]
		d.close()

		return removed, added, items 

if __name__ == "__main__":
	"""
	below is just a cooked up sample of how the collection
	object can be used	
	"""

	mycollection = collection('mycollection.db')
	removed, added, items = mycollection(('b','c','d'))

	if removed:
		print "\nitem(s) removed from the collection:\n"
		for item in removed:
			print "\t%s" % item
	if added:
		print "\nitem(s) added to the collection:\n"
		for item in added:
			print "\t%s" % item

	if items:
		print "\nitem(s):\n"
		for item in items:
			i, age = item
			print "\titem: %-12s age: %s" % (i,age)
