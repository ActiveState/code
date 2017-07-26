#!/usr/bin/env python
#title			:passwdcard.py
#description	        :This will generate a unique credit card sized random grid 
#                       :of characters that can be used to create secure passwords.
#author                 :bgw
#date			:20120110
#version		:0.1
#usage			:python passwdcard.py
#notes			:This was insprired by the website: passwordcard.org
#python_version	        :2.6.6
#=============================================================================

import random  
from os.path import exists

# The random characters will be selected from this list.
char = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", 
		"o", "p", "q", "r", "s", "t", "u", "v", "x", "y", "z", "1", "2", "3", 
		"4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "E", "F", "G", 
		"H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", 
		"V", "X", "Y", "Z", '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
		'[', ']', '{', '}', '/', '=', '+', '_', '-', '<', '>', '.', '\'', '\"', 
		'\\' ]

# Top row of the card.
row = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
			"n", "o", "p", "q", "r", "s", "t" ]
            
pcard = "passwdcard.txt"

# Check to see if the file already exists!
if exists(pcard):
    overwrite = raw_input("Do you want to overwrite the %s file? (y or n)\n" % \
    pcard)
    if overwrite == "n":
        print "The file will not be overwritten."
        exit(1)
    else:
        print "The file has been overwritten!"

# Create the file passwdcard.txt.
filename = open(pcard, 'w')

# Write to the file.
filename.write("\t%s\n" % ' '.join(row))
filename.write("\t%s\n" % "---------------------------------------")
filename.write("01. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("02. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("03. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("04. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("05. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("06. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("07. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("08. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("09. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("10. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("11. %s\n" % ' '.join(random.sample(char, 20)))
filename.write("12. %s\n" % ' '.join(random.sample(char, 20)))

# Close the file after writing to it.
filename.close()
