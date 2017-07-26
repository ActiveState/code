#!/usr/bin/env python
# A simple game. auth: DR#m; last rev: 17-04
# Rules: CPU and man are dropping dices
# 	if someone scores > 17, he looses
import random
global manSum;			manSum=0
global compSum;			compSum=0
global manFinished;		manFinished=False
global CPUfinished;		CPUfinished=False
global gameover;		gameover=False
global debug;			debug=False	# some additional info about game flow

def dice():
	"""Number of points in dice"""
	return random.randint(1,6)

def looser(who):
	"""Finishes the game"""
	global manSum, compSum, gameover
	print
	if who=="man":
		print "LOOSER"
	elif who=="CPU":
		print "Congratulations!"
	print
	print "your score: ", manSum
	print "CPU score: ", compSum
	gameover = True;

def testWinLoose():
	"""Complicated test- if somebody won?"""
	global manSum, compSum, debug
	if (compSum >= 18):
		looser("CPU")
	elif (manSum >= 18):
		looser("man");
	else:
		if (manSum == 17):
			looser("CPU")
		elif (compSum == 17):
			looser("man")
		else: # nobody wants to play ?
			if (manFinished and CPUfinished):
				manCount = 17 - manSum
				compCount = 17 - compSum
				if debug:
					print "score testing: "
				if manCount > compCount:
					looser("man")
				else: looser("CPU")
def CPUdrop():
	""" CPU drops his dice.
		The algorithm is following:
		guess the next number in dice (randomly)
		and drop dice again to increase score
		if you want to cheat, put "+1" somewhere here ;-)
	"""
	global CPUfinished, manSum, compSum, debug
	if (not CPUfinished):	# already refused
		NeedPoints = 17 - compSum	# how much we need?
		if (dice() <= NeedPoints):	# probability is well today
			compSum += dice() # dice() is called twice, should return different values
			if debug:
				print "CPU played. His points: ", compSum
		else:	# too big score
			CPUfinished = True	# enough points
			if debug:
				print "CPU refused. His points: ", compSum

print "You are welcome!"
for a in xrange(3):	# first tree drops
	manSum+=dice()
	compSum+=dice()
while (not gameover):
	if (not manFinished):
		# let`s print the menu for user
		print "Ur score", manSum
		if (debug): 	# usually, opponent`s score is unknown
			print "CPU score", compSum
		print "1: Drop!"
		print "2: Enough!"
		print "or give up"
		inp=raw_input()
		if inp == "1":			# dice dropping
			manSum += dice()
		elif inp == "2":
			manFinished = True	# man- enough
		else:	# all other input is forbidden :))
			if (debug):
				print "Why`ve you gived up?"
			looser("man")
	else: #if (not manFinished)
		if (debug):
			print "Scipping menu..."
	CPUdrop(); # CPU plays after

	testWinLoose(); # after dice dropping

print "hit Enter to exit!"
raw_input()
