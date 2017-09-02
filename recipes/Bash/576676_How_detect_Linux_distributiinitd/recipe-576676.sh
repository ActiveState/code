#!/bin/bash

LSB=$( which lsb_release )

if [[ ! ${LSB} ]]; then

	echo "LSB is not installed. Unable to determine your distribution."
	exit

else

	${LSB} -a | grep -v LSB

fi