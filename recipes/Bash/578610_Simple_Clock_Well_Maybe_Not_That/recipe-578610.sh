#!/bin/bash
#
# Clock_DEMO.sh
# A bash DEMO to create a 6 x 7 character set using the whitespace character.
# It is a functional digital clock but this is not important as I want this
# method for an _at_a_glance_ digital display for a kids level shell digital
# voltmeter I am in the process of doing.
#
# The clock in normal size is white on black near the top. The extra large clock
# is green on black and in the centre of the terminal..
#
# $VER: Clock.sh_Version_1.00.00_(C)2013_B.Walker_G0LCU.
#
# Written so the anyone can understand how it works.

# Set the window to white foreground on black background.
printf "\x1B[0;37;40m"
clear
# Remove the cursor.
tput civis
# Set up all _variables_ as is required.
TIME=`date "+%H:%M"`
char="0"
# The plot _variable_ "p".
p="(C)2013, B.Walker, G0LCU."
# The background colours.
bg="\x1B[0;37;40m"
# The foreground colours.
fg="\x1B[0;37;42m"
# The initial character plotting points.
horiz=10
vert=9
# This function reads the time and stores it in "TIME".
clock()
{
	TIME=`date "+%H:%M"`
	printf "\x1B[2;32f$bg The time is $TIME.\n"
}
# This function is required to coreectly print out the large characters.
plot()
{
	p="\x1B["$vert";"$horiz"f"
	vert=$[ ( $vert + 1 ) ]
}
# *********************************************************
# The eleven characters required for this DEMO are 0 to 9
# and the : colon character.
zero()
{
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$fg $bg  $fg  $bg "
	plot
	printf "$p$fg $bg $fg $bg $fg $bg "
	plot
	printf "$p$fg  $bg  $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
}
one()
{
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg  $fg  $bg  "
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg  $fg   $bg "
}
two()
{
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$fg     $bg "
}
three()
{
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
}
four()
{
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg  $fg  $bg  "
	plot
	printf "$p$bg $fg $bg $fg $bg  "
	plot
	printf "$p$fg $bg  $fg $bg  "
	plot
	printf "$p$fg     $bg "
	plot
	printf "$p$bg   $fg $bg "
	plot
	printf "$p$bg   $fg $bg "
}
five()
{
	plot
	printf "$p$fg     $bg "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
}
six()
{
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$fg    $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
}
seven()
{
	plot
	printf "$p$fg     $bg "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$bg   $fg $bg  "
	plot
	printf "$p$bg  $fg $bg   "
	plot
	printf "$p$bg $fg $bg    "
	plot
	printf "$p$fg $bg     "
	plot
	printf "$p$fg $bg     "
}
eight()
{
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
}
nine()
{
	plot
	printf "$p$bg $fg   $bg  "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$fg $bg   $fg $bg "
	plot
	printf "$p$bg $fg    $bg "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$bg    $fg $bg "
	plot
	printf "$p$bg $fg   $bg  "
}
colon()
{
	plot
	printf "$p$bg      "
	plot
	printf "$p$bg      "
	plot
	printf "$p$bg  $fg $bg   "
	plot
	printf "$p$bg      "
	plot
	printf "$p$bg  $fg $bg   "
	plot
	printf "$p$bg      "
	plot
	printf "$p$bg      "
}
# End of the character set.
# *********************************************************
# Print all of these characters first just to display them.
# This will last for 5 seconds only...
# Done longhand purely for fun...
horiz=10
vert=9
zero
horiz=16
vert=9
one
horiz=22
vert=9
two
horiz=28
vert=9
three
horiz=34
vert=9
four
horiz=40
vert=9
five
horiz=46
vert=9
six
horiz=52
vert=9
seven
horiz=58
vert=9
eight
horiz=64
vert=9
nine
horiz=70
vert=9
colon
# Now display the clock in the normal character size...
clock
sleep 5
# Now clear the screen and display the big digits.
clear
while true
do
	clock
	for subscript in $( seq 0 1 4)
	do
		# Take each character in turn and do the plots of them.
		char="${TIME:${subscript}:1}"
		horiz=$[ ( 26 + ( $subscript * 6 ) ) ]
		vert=9
		if [ "$char" == ":" ]
		then
			colon
		fi
		if [ "$char" == "0" ]
		then
			zero
		fi
		if [ "$char" == "1" ]
		then
			one
		fi
		if [ "$char" == "2" ]
		then
			two
		fi
		if [ "$char" == "3" ]
		then
			three
		fi
		if [ "$char" == "4" ]
		then
			four
		fi
		if [ "$char" == "5" ]
		then
			five
		fi
		if [ "$char" == "6" ]
		then
			six
		fi
		if [ "$char" == "7" ]
		then
			seven
		fi
		if [ "$char" == "8" ]
		then
			eight
		fi
		if [ "$char" == "9" ]
		then
			nine
		fi
	done
	sleep 1
done
# There is no code to clean up the terminal for this session in this DEMO.
# It is SOOO easy to do it manually that I expect you to be able to do
# that yourselves.
# Enjoy finding simple solutions to often very difficult questions.
