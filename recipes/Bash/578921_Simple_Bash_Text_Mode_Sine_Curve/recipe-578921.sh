#!/bin/bash
# plotsine.sh
# A DEMO to display a sinewave inside a standard bash terminal.
# Issued as Public Domain, 2014, B.Walker, G0LCU.
# Device: Macbook Pro 13", OSX 10.7.5, default bash terminal.
# Use variables so that you can see how it works.
angle=0
step_angle=5
vert_plot=0
horiz_plot=5
centreline=12
amplitude=11
PI=3.14159
clear
# Do a single cycle, quantised graph.
while [ $angle -le 359 ]
do
	# Create each floating point value...
	# CygWin now catered for... ;o)
	vert_plot=$(awk "BEGIN{ printf \"%.12f\", ((sin($angle*($PI/180))*$amplitude)+$centreline)}")
	#vert_plot=$(bc -l <<< "{print ((s($angle*($PI/180))*$amplitude)+$centreline)}")
	# Truncate the floating point value to an integer then invert the plot to suit the x y co-ordinates inside a terminal...
	vert_plot=$((24-${vert_plot/.*}))
	# Plot the point(s) and print the angle at that point...
	printf "\x1B["$vert_plot";"$horiz_plot"f*"
	printf "\x1B[22;1fAngle is $angle degrees..."
	sleep 0.1
	# Increment values...
	angle=$((angle+step_angle))
	horiz_plot=$((horiz_plot+1))
done
printf "\x1B[23;1fSinewave plotted as a quantised text mode graph.\n"
exit 0
#
#                  *********
#               ***         ***
#              *               *
#            **                 **
#           *                     *
#          *                       *
#         *                         *
#        *                           *
#       *                             *
#      *                               *
#    **                                 **
#                                         *                                 *
#                                          *                               *
#                                           *                             *
#                                            *                           *
#                                             *                         *
#                                              *                       *
#                                               *                     *
#                                                **                 **
#                                                  *               *
#Angle is 355 degrees...                            ***         ***
#Sinewave plotted as a quantised text mode graph.      *********
#AMIGA:barrywalker~> _
