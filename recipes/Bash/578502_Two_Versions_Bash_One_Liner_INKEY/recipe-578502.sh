Version one...
Edit out as resquired...

#!/bin/bash

# An INKEY$ function for bash!
inkey() { char="" ; read -p "" -n1 -s -t1 char ; }
# Similar to BASIC's LET char$=INKEY$

# Do you remember INKEY$ in BASIC programming?
# Example:-
#
# PRINT "Some prompt:- "
# some_label:
# LET char$=INKEY$
# IF char$="<some_character>" THEN <do_something>
# IF char$="" THEN <do_something_else>
# GOTO some_label

# This is just a test piece only...
while true
do
	printf "Some prompt:- "
	# This is LET char$=INKEY$...
	inkey
	printf "$char...\n"
	if [ "$char" == "q" ]
	then
		printf "\nQuitting...\n\n"
		break
	fi
	if [ "$char" == "" ]
	then
		printf "Timeout works OK...\n"
	fi
	if [ "$char" == "b" ]
	then
		printf "Barry Walker...\n"
	fi
done



Version two...
Edit out as required...

#!/bin/bash

# Another INKEY$ function for bash!
inkey() { char="" ; stty -icanon min 0 time 1 ; char=`dd count=1 2> /dev/null` ; }
# Similar to BASIC's LET char$=INKEY$

# Do you remember INKEY$ in BASIC programming?
# Example:-
#
# PRINT "Some prompt:- "
# some_label:
# LET char$=INKEY$
# IF char$="<some_character>" THEN <do_something>
# IF char$="" THEN <do_something_else>
# GOTO some_label

while true
do
	printf "Some prompt:- "
	# This is LET char$=INKEY$...
	inkey
	printf "$char...\n"
	if [ "$char" == "q" ]
	then
		printf "\nQuitting... \n\n"
		break
	fi
	if [ "$char" == "" ]
	then
		printf "Timeout works OK...\n"
	fi
	if [ "$char" == "b" ]
	then
		printf "Barry Walker...\n"
	fi
done
