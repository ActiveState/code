#!/usr/bin/python

from bsddb3 import db                   # the Berkeley db data base

# Part 1: Create database and insert 4 elements
#
filename = 'fruit'

# Get an instance of BerkeleyDB 
fruitDB = db.DB()
# Create a database in file "fruit" with a Hash access method
# 	There are also, B+tree and Recno access methods
fruitDB.open(filename, None, db.DB_HASH, db.DB_CREATE)

# Print version information
print '\t', db.DB_VERSION_STRING

# Insert new elements in database 
fruitDB.put("apple","red")
fruitDB.put("orange","orange")
fruitDB.put("banana","yellow")
fruitDB.put("tomato","red")

# Close database
fruitDB.close()

# Part 2: Open database and write its contents out
#
fruitDB = db.DB()
# Open database
#	Access method: Hash
#	set isolation level to "dirty read (read uncommited)"
fruitDB.open(filename, None, db.DB_HASH, db.DB_DIRTY_READ)

# get database cursor and print out database content
cursor = fruitDB.cursor()
rec = cursor.first()
while rec:
        print rec
        rec = cursor.next()
fruitDB.close()
