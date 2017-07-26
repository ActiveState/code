# SimpleTron3x.py
#
# Yes I know it is not much of a game but it is intended to show how to
# "draw", AND, to use the keyboard to "draw" inside a standard text mode
# Python shell.
#
# Written in such a way as to easily understand how it works.
#
# IMPORTANT NOTE!!! This ASSUMES a standard 80 x 24 shell window.
#
# This working idea is copyright, (C)2011, B.Walker, G0LCU.
# NOW issued as Public Domain...
#
# To run at the prompt...
# >>> exec(open("/full/path/to/SimpleTron3x.py").read())

def main():
	import os
	import sys
	import termios
	import tty
	import random

	# A basic clear screen and cursor removal for program start...
	os.system("clear")
	os.system("setterm -cursor off")

	# Make any variables global just for this DEMO "game"...
	global screen_array
	global character
	global line
	global position
	global remember_attributes
	global plot
	global inkey_buffer
	global score

	screen_array="*"
	character="a"
	remember_attributes="(C)2011, B.Walker, G0LCU."
	line=1
	position=0
	plot=int(random.random()*4)
	inkey_buffer=0
	score=0

	# This is a working function; something akin to the BASIC INKEY$ function...
	# Reference:- http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
	# Many thanks to Danny Yoo for the above code, modified to suit this program...
	# In THIS FUNCTION some special keys do a "break" similar to the "Esc" key inside the program.
	# Be aware of this...
	# An inkey_buffer value of 0, zero, generates a "" character and carries on instead of waiting for
	# a valid ASCII key press.
	def inkey():
		fd=sys.stdin.fileno()
		remember_attributes=termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())
		character=sys.stdin.read(inkey_buffer)
		termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
		return character

	# The welcome screen.
	print("")
	print("SimpleTron3x.py. A simple, odd style, Tron(ish) game.")
	print("Another DEMO 2D animation for Linux platforms.")
	print("")
	print("You control a vehicle leaving a trail behind it.")
	print("")
	print("It is NOT always moving, and if it crosses any part")
	print("of the trail or border, (* characters), the game")
	print("is over. It CAN randomly move further than the key")
	print("presses so do not assume there is a bug... :)")
	print("Use the Q and A keys to change the direction to")
	print("up and down, and O and P for left and right.")
	print("See how long you can survive! Score at the end.")
	print("")
	character=input("Hit <RETURN/ENTER> to begin... ")

	# Generate the game window as a single text string.
	# This assumes a standard 80x24 terminal text window.
	# Top line.
	while position<=78:
		screen_array=screen_array+"*"
		position=position+1
	# Next 20 lines.
	while line<=20:
		position=1
		screen_array=screen_array+"*"
		while position<=78:
			screen_array=screen_array+" "
			position=position+1
		screen_array=screen_array+"*"
		line=line+1
	screen_array=screen_array+"*"
	# Bottom line.
	position=0
	while position<=78:
		screen_array=screen_array+"*"
		position=position+1

	# Store the complete string for future use.
	gamefile=open("/tmp/TronArray","w+")
	gamefile.write(screen_array)
	gamefile.close()
	# End of game setup...

	# Start of game proper, set the initial position.
	position=(int(random.random()*60)+890)
	while 1:
		# Standard clear the terminal window.
		os.system("clear")
		print(screen_array)
		# Add another * when inkey_buffer=0.
		inkey_buffer=int(random.random()*2)
		# Use the INKEY$ function to grab an ASCII key.
		character=inkey()
		if character=="a": plot=0
		if character=="A": plot=0
		if character=="q": plot=1
		if character=="Q": plot=1
		if character=="o": plot=2
		if character=="O": plot=2
		if character=="p": plot=3
		if character=="P": plot=3
		# Esc key to exit the loop...
		if character==chr(27): break
		if plot==0: position=position+80
		if plot==1: position=position-80
		if plot==2: position=position-1
		if plot==3: position=position+1
		if position>=1759: position=1759
		if position<=0: position=0

		gamefile=open("/tmp/TronArray","r+")
		# Check for a * character in the array and......
		gamefile.seek(position)
		if gamefile.read(1)=="*":
			# ......exit if one exists at that point.
			gamefile.close()
			print("Game Over! You scored",score,"\b...")
			break
		gamefile.seek(position)
		gamefile.write("*")
		# Now get the whole array.
		gamefile.seek(0)
		screen_array=gamefile.read(1760)
		gamefile.close()
		# End of screen_array update per plot.
		score=score+1

	# Reset the cursor, etc...
	os.system("setterm -cursor on")
	character=input("Have another game? (Y/N):- ")
	if character=="y": main()
	if character=="Y": main()
	if character=="": main()

main()

# SimpleTron3x.py end of game.
# Enjoy finding simple solutions to often very difficult questions.
