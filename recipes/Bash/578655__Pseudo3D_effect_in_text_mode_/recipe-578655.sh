Linux version:-

Code:

#!/bin/bash --posix
# This DEMO generates a simple pseudo-3D recessed or raised box in text
# mode format...
#
# Tested on PCLinuxOS 2009 and Debian 6.0.x on their default terminals...
# Checked on a Macbook Pro, 13 inch, OSX 10.7.5 on its default terminal...
vert=1
horiz=1
text1="This is the first line."
text2="This is the second line."
# Bright white on light grey...
printf "\x1B[1;37;47m"
clear

plot()
{
	printf "\x1B["$vert";"$horiz"f"
}

box()
{
	plot
	printf "\x1B[0;30;47m+-----------------------------------\x1B[1;37;47m+"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[0;30;47m|                                   \x1B[1;37;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[0;30;47m|                                   \x1B[1;37;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[0;30;47m+\x1B[1;37;47m-----------------------------------+"
}

button()
{
	plot
	printf "\x1B[1;37;47m+-----------------------------------\x1B[0;30;47m+"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[1;37;47m|                                   \x1B[0;30;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[1;37;47m|                                   \x1B[0;30;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[1;37;47m+\x1B[0;30;47m-----------------------------------+"
}

# Simple program start...
# Set the box and button positions first...
vert=4
horiz=22
box
vert=9
horiz=22
button
# Now plot the two text lines...
vert=5
horiz=24
plot
printf "\x1B[0;32;47m$text1"
vert=6
horiz=24
plot
printf "\x1B[0;31;47m$text2\n\n\n"
vert=10
horiz=24
plot
printf "\x1B[0;34;47m$text1"
vert=11
horiz=24
plot
printf "\x1B[0;30;47m$text2\n\n\n"



Macbook Pro version:-

Code:

#!/bin/bash --posix
# This DEMO generates a simple pseudo-3D recessed or raised box in text
# mode format...
# 
# For a Macbook Pro, 13 inch, OSX 10.7.5...
vert=1
horiz=1
text1="This is the first line."
text2="This is the second line."
# Bright white on light grey...
printf "\x1B[1;97;47m"
clear

plot()
{
	printf "\x1B["$vert";"$horiz"f"
}

box()
{
	plot
	printf "\x1B[0;30;47m+-----------------------------------\x1B[1;97;47m+"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[0;30;47m|                                   \x1B[1;97;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[0;30;47m|                                   \x1B[1;97;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[0;30;47m+\x1B[1;97;47m-----------------------------------+"
}

button()
{
	plot
	printf "\x1B[1;97;47m+-----------------------------------\x1B[0;30;47m+"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[1;97;47m|                                   \x1B[0;30;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[1;97;47m|                                   \x1B[0;30;47m|"
	vert=$[ ( $vert + 1 ) ]
	plot
	printf "\x1B[1;97;47m+\x1B[0;30;47m-----------------------------------+"
}

# Simple program start...
# Set the box and button positions first...
vert=4
horiz=22
box
vert=9
horiz=22
button
# Now plot the two text lines...
vert=5
horiz=24
plot
printf "\x1B[0;32;47m$text1"
vert=6
horiz=24
plot
printf "\x1B[0;31;47m$text2\n\n\n"
vert=10
horiz=24
plot
printf "\x1B[0;34;47m$text1"
vert=11
horiz=24
plot
printf "\x1B[0;30;47m$text2\n\n\n"
