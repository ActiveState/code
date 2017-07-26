#!/usr/bin/python
import argparse
import random

parser = argparse.ArgumentParser(description='Generate a left-handed random password.')

parser.add_argument('-n', action='store', dest='passNum', default=8, type=int, help='Number of passwords to generate.')
parser.add_argument('-l', action='store', dest='passLen', default=8, type=int, help='Length of password')
parser.add_argument('-s', action='store', dest='passStrength', default=4, type=int, help='Strength of password (1-4)')

lowerChars = "qwertasdfgzxcvb"
upperChars = "QWERTASDFGZXCVB"
lowerNum = "123456"*3 # repeated digits for 'weight'
upperNum = '!"$%^'*3

results=parser.parse_args()

#Generate character to select from according to passStrength (-s)
if results.passStrength == 1:
	leftHand = lowerChars
elif results.passStrength == 2:
	leftHand = lowerChars+upperChars
elif results.passStrength == 3:
	leftHand = lowerChars+upperChars+lowerNum
elif results.passStrength == 4:
	leftHand = lowerChars+upperChars+lowerNum+upperNum

for i in range(results.passNum):
	leftPass = ''
	for j in range(results.passLen):
		leftPass = leftPass + leftHand[random.randint(0,len(leftHand)-1)]
	print leftPass
