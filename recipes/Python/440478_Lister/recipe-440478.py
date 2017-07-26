#!/usr/bin/python
# Filename : lister.py

import sys, pickle

global mylist
mylist = []

def takeinput():
	# take input from user to select which function
	try:	
		num = int(raw_input('--> '))
		if num == 1:
			printlist()
		elif num == 2:
			add()
		elif num == 3:
			delete()
		elif num == 4:
			save()
		elif num == 5:
			load()
		elif num == 6:
			quit()
		else:
			quit()
	except ValueError:
		quit()
	

def printlist():
	# print mylist
	print 'mylist is now:', mylist, '\n'

def add():
	# add an item to mylist
	s = str(raw_input('Enter the name of the object you want to add --> '))
	mylist.append(s) # add the 
	del s
	printlist()

def delete():
	# delete an item from mylist
	print # newline
	i = 0
	while i < len(mylist): 		  # use while loop to assign 'itm' to the  
		for itm in mylist:	  # items in the list. Then, print the number of  
			print itm,'is',i  # items and items in mylist.  
			i = i + 1	  # the numbers of the items and items is printed.
	
	print # newline
	s = int(raw_input('Enter the number of the object you want to delete --> '))
	del mylist[s] # delete the item using both 'del' function & indexing method
	del s	
	printlist()
	
def save():
	# save mylist
	mylist_data = 'lister.data' # The name of the file
	f =  file(mylist_data, 'w') # Open for 'w'riting
	pickle.dump(mylist, f) # dump/put the list into the file
	f.close()	       # close
	print 'Saved mylist :)'

def load():
	# load mylist
	mylist_data = 'lister.data'
	f = file(mylist_data)
	storedlist = pickle.load(f)
	print 'Loaded mylist :)'

def quit():
	# quit the program
	print 'Bye! :) \n'
	sys.exit()

# Script starts here
	
print '''\
Hi! this is a lister program.
Type:
1- print mylist
2- add an object to mylist
3- delete an object from mylist
4- save mylist
5- load mylist
6- quit\
'''

running = True

while running:
	takeinput() # Always take input from user until he/she quits the program
