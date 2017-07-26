#!/bin/bash
#
# Bargraph_Generator.sh
#
# A DEMO 6 bit coloured bargraph animation for a default Bash and Terminal window on OSX 10.7.5...
# A simple Shell script to display an _AT_A_GLANCE_ real time analogue bargraph generator. It
# starts off with GREEN for OK, then YELLOW for warning and finally ending with RED for danger
# with a critical beep for values 61 to 63 inclusive.
# It assumes an 8 bit value being injected into the script which is then divided by 4 to give
# a 6 bit value which is 64 spaces width inside the Terminal. The DEMO uses a random number
# generator to give a representation of an 8 bit value so you can see it working...
#
# A shell derivative of my Python code:-
# http://code.activestate.com/recipes/577612-seven-bit-colored-analogue-bar-graph-generator-dem/?in=user-4177147
#
# To run, ensure the script is executable and change if required, then type from a Terminal:-
#
# xxxxx$ /full/path/to/Bargrapth_Generator.sh<CR>
#
# And away you go...
#
# Written in such a way that kids and newbies can understand what is going on.
#
# Originally written for a Macbook Pro 13 inch, OSX 10.7.5 using the default Terminal.
# It MIGHT work on some Linux variants but WAS intended for MacOS OSX 10.7.x and above only.
#
# The Terminal colours WILL be changed to Black background and Various foreground colours.
# It will NOT be returned back to its original state although it can be easily. If you
# need to rerturn back to default state then there are a couple of easy methods the
# simplest being type:-
#
# xxxxx$ reset<CR>
#
# And all will be corrected...
#
# Issued entirely as Public Domain and you may do with it as you please
#
# $VER Bargraph_Generator.sh_Version_0.00.10_(C)2012_B.Walker_G0LCU.
#
# Enjoy finding simple solutions to often very difficult problems...

# The required _varibales_ for ease of coding, these are the colours...
# White On Black.
WOB="\x1B[1;37;40m"
# Black On Green.
BOG="\x1B[1;30;42m"
# Black On Yellow.
BOY="\x1B[1;30;43m"
# Black On red.
BOR="\x1B[1;30;41m"
# Green On Black.
GOB="\x1B[1;32;40m"
# Yellow On Black.
YOB="\x1B[1;33;40m"
# Red On Black.
ROB="\x1B[1;31;40m"

# Set the pseudo 6 bit value to zero.
SIX_BIT_DEPTH=0

# Do a clear screen to White On Black.
printf $WOB
clear

while true
do
	# Set up the screen per scan and prepare for the bargraph.
	clear
	printf $WOB"\n \$VER: Bargraph_Generator.sh_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n\n"
	printf " A horizontal, at a glance, coloured, analogue bargraph display for\n"
	printf " a default Terminal inside OSX 10.7.5..\n\n\n\n\n"
	printf "        0         10        20        30        40        50        60"
	printf $GOB"\n        +----+----+----+----+----+----+----+----+----+"$YOB"----+----+"$ROB"----+--\n"
	printf $GOB"       (|                                                              "$ROB")\n"
	printf $GOB"        +----+----+----+----+----+----+----+----+----+"$YOB"----+----+"$ROB"----+--\n\n\n\n"
	# If the 6 bit value is 0, zero, do no more until printing the 6 bit value and generating another 6 bit value...
	# Anything greater than or equal to 1 enters this conditional branch.
	if [ "$SIX_BIT_DEPTH" -ge "1" ]
	then
		# If the 6 bit value is less than or equal to 46 then _plot_ the green section only.
		# The '\x1B[12;8f' is the ANSI 'Esc' code that forces the print position to 12 lines by 8 columns.
		if [ "$SIX_BIT_DEPTH" -le "46" ]
		then
			BARGRAPH=$GOB"\x1B[12;8f("$BOG
			for green in $(seq 1 "$SIX_BIT_DEPTH")
			do
				BARGRAPH=$BARGRAPH" "
			done
		fi
		# If the 6 bit value is greater than or equal to 47 then print the green section and _plot_ the yellow section.
		if [ "$SIX_BIT_DEPTH" -ge "47" ]
		then
			BARGRAPH=$GOB"\x1B[12;8f("$BOG"                                              "$BOY
			for yellow in $(seq 47 "$SIX_BIT_DEPTH")
			do
				BARGRAPH=$BARGRAPH" "
			done
		fi
		# If the 6 bit value is greater than or equal to 57 then print the green and yellow section and _plot_ the red section.
		if [ "$SIX_BIT_DEPTH" -ge "57" ]
		then
			BARGRAPH=$GOB"\x1B[12;8f("$BOG"                                              "$BOY"          "$BOR
			for red in $(seq 57 "$SIX_BIT_DEPTH")
			do
				BARGRAPH=$BARGRAPH" "
			done
		fi
		printf "$BARGRAPH"$GOB"\n\n\n\n\n"
	fi
	# When the 6 bit value is greater than or equal to 61 sound a system error beep.
	if [ "$SIX_BIT_DEPTH" -ge "61" ]
	then
		printf "\a"
	fi
	# Print the 6 bit value in White On Black...
	printf $WOB" Random number generated "$SIX_BIT_DEPTH"...\n\n"
	printf " Press Ctrl-C to stop the program...\n\n"
	# Generate another 6 bit value as though from an 8 bit value...
	SIX_BIT_DEPTH=$[($RANDOM % (256/4))]
	# A practical lower limit for the sleep command is 'sleep 0.05'...
	sleep 1
done

# End of Bargraph_Generator.sh DEMO.
# Enjoy finding simple solutions to often very difficult problems... ;o)
