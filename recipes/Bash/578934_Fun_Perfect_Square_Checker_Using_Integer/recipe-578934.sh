#!/bin/bash
# perfect_square <number>
number=$1
if [ "$number" -eq "$number" ] > /dev/null 2>&1 
then
	if [ $number -lt 0 ]
	then
		echo "Warning! Integer is negative!!!"
		echo "Set input integer to the DEMO value of 99..."
		number=99
	fi
else
	echo "Invalid Argument! Set input integer to the DEMO value of 100..."
	number=100
fi
series=1
square=1
root=1
while true
do
	if [ $square -le $number ]
	then
		if [ $square -eq $number ]
		then
			echo "$number is the perfect square of $root..."
			exit 0
		fi
		root=$((root+1))
		series=$((series+2))
		square=$((square+series))
	else
		echo "Integer $number is not a perfect square..."
		exit 1
	fi
done
exit 0
# Last login: Tue Sep 16 20:12:27 on ttys000
# AMIGA:barrywalker~> chmod 755 perfect_square
# AMIGA:barrywalker~> ./perfect_square ierooeirt
# Invalid Argument! Set input integer to the DEMO value of 100...
# 100 is the perfect square of 10...
# AMIGA:barrywalker~> ./perfect_square -345
# Warning! Integer is negative!!!
# Set input integer to the DEMO value of 99...
# Integer 99 is not a perfect square...
# AMIGA:barrywalker~> ./perfect_square 0
# Integer 0 is not a perfect square...
# AMIGA:barrywalker~> ./perfect_square 123.9
# Invalid Argument! Set input integer to the DEMO value of 100...
# 100 is the perfect square of 10...
# AMIGA:barrywalker~> ./perfect_square 625
# 625 is the perfect square of 25...
# AMIGA:barrywalker~> ./perfect_square 1
# 1 is the perfect square of 1...
# AMIGA:barrywalker~> ./perfect_square 11111
# Integer 11111 is not a perfect square...
# AMIGA:barrywalker~> ./perfect_square oiwero11234ldkf
# Invalid Argument! Set input integer to the DEMO value of 100...
# 100 is the perfect square of 10...
# AMIGA:barrywalker~> ./perfect_square -0.0
# Invalid Argument! Set input integer to the DEMO value of 100...
# 100 is the perfect square of 10...
# AMIGA:barrywalker~> ./perfect_square -1.25
# Invalid Argument! Set input integer to the DEMO value of 100...
# 100 is the perfect square of 10...
# AMIGA:barrywalker~> ./perfect_square -1
# Warning! Integer is negative!!!
# Set input integer to the DEMO value of 99...
# Integer 99 is not a perfect square...
# AMIGA:barrywalker~> _
