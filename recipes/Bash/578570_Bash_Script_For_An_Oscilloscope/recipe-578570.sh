#!/bin/bash
#
# AudioScope.sh
#
# At this point I will include and say thank you to "Corona688", a member of http://www.unix.com for his input...
# Also to others on the same site for their input too.
# Many thanks also go to the guys who have helped with this on http://www.linuxformat.com for all your input too...
#
# Tested in SOX mode on this Macbook Pro 13 inch, OSX 10.7.5 with the SOX sinewave generator enabled.
# Tested in /dev/dsp mode on an aging HP notebook running Debian 6.0.x with the /dev/dsp sinewave generator enabled.
# Tested in /dev/dsp mode on an Acer Aspire One netbook booting from a USB stick running PCLinuxOS 2009; also with
# the /dev/dsp sinewave generator enabled.
# Tested on all three in DEMO mode.
#
# Added the first simple circuit at the end of this script.
#
# Relevant pointers to help:-
# http://wisecracker.host22.com/public/AudioScope_Manual.readme
# http://wisecracker.host22.com/public/cal_draw.jpg
# http://wisecracker.host22.com/public/cal_plot.jpg
# http://wisecracker.host22.com/public/mic_ear1.jpg
# http://wisecracker.host22.com/public/mic_ear2.jpg
# http://wisecracker.host22.com/public/mic_ear3.jpg
# http://wisecracker.host22.com/public/mic_ear4.jpg
#
# The latest vesrion will always be here:-
# http://www.unix.com/shell-programming-scripting/212939-start-simple-audio-scope-shell-script.html
#
# NOTE TO SELF:- Remove "/tmp" and replace with "~" when ready, AND, "/tmp" is automatically cleared on this machine per reboot.

# #########################################################
# FOR SOund eXchance USERS ONLY!!!        TESTED!!!
# The lines below, from ">" to "xterm", will generate a new shell script and execute it in a new xterm terminal...
# Just EDIT out the comments and then EDIT the line pointing to the correct </full/path/to/sox/> to use it.
# It assumes that you have SoX installed. When this script is run it generates a 1KHz sinewave in a separate window
# that lasts for 8 seconds. Just press ENTER when this window is active and it will repeat again. To quit this script
# and close the window just press Ctrl-C. This generator will be needed for the calibration of some timebase ranges. 
#> /tmp/1KHz-Test.sh
#chmod 744 /tmp/1KHz-Test.sh
#printf '#!/bin/bash\n' >> /tmp/1KHz-Test.sh
#printf '> /tmp/sinewave.raw\n' >> /tmp/1KHz-Test.sh
#printf 'data="\\\\x80\\\\x26\\\\x00\\\\x26\\\\x7F\\\\xD9\\\\xFF\\\\xD9"\n' >> /tmp/1KHz-Test.sh
#printf 'for waveform in {0..8191}\n' >> /tmp/1KHz-Test.sh
#printf 'do\n' >> /tmp/1KHz-Test.sh
#printf '        printf "$data" >> /tmp/sinewave.raw\n' >> /tmp/1KHz-Test.sh
#printf 'done\n' >> /tmp/1KHz-Test.sh
#printf 'while true\n' >> /tmp/1KHz-Test.sh
#printf 'do\n' >> /tmp/1KHz-Test.sh
#printf '        /full/path/to/sox/play -b 8 -r 8000 -e unsigned-integer /tmp/sinewave.raw\n' >> /tmp/1KHz-Test.sh
#printf '        read -p "Press ENTER to rerun OR Ctrl-C to quit:- " -e kbinput\n' >> /tmp/1KHz-Test.sh
#printf 'done\n' >> /tmp/1KHz-Test.sh
#sleep 1
#xterm -e /tmp/1KHz-Test.sh &

# #########################################################
# FOR /dev/dsp USERS ONLY!!!           TESTED!!!
# The lines below, from ">" to "xterm", will generate a new shell script and execute it in a new xterm terminal...
# Just EDIT out the comments to use it.
# It assumes that you have /dev/dsp _installed_. When this script is run it generates a 1KHz sinewave in a separate window
# that lasts for 8 seconds. Just press ENTER when this window is active and it will repeat again. To quit this script
# and close the window just press Ctrl-C. This generator will be needed for the calibration of some timebase ranges. 
#> /tmp/1KHz-Test.sh
#chmod 744 /tmp/1KHz-Test.sh
#printf '#!/bin/bash\n' >> /tmp/1KHz-Test.sh
#printf '> /tmp/sinewave.raw\n' >> /tmp/1KHz-Test.sh
#printf 'data="\\\\x80\\\\x26\\\\x00\\\\x26\\\\x7F\\\\xD9\\\\xFF\\\\xD9"\n' >> /tmp/1KHz-Test.sh
#printf 'for waveform in {0..8191}\n' >> /tmp/1KHz-Test.sh
#printf 'do\n' >> /tmp/1KHz-Test.sh
#printf '        printf "$data" >> /tmp/sinewave.raw\n' >> /tmp/1KHz-Test.sh
#printf 'done\n' >> /tmp/1KHz-Test.sh
#printf 'while true\n' >> /tmp/1KHz-Test.sh
#printf 'do\n' >> /tmp/1KHz-Test.sh
#printf '        cat /tmp/sinewave.raw > /dev/dsp\n' >> /tmp/1KHz-Test.sh
#printf '        read -p "Press ENTER to rerun OR Ctrl-C to quit:- " -e kbinput\n' >> /tmp/1KHz-Test.sh
#printf 'done\n' >> /tmp/1KHz-Test.sh
#sleep 1
#xterm -e /tmp/1KHz-Test.sh &

# #########################################################
# Variables in use.
ifs_str=$IFS
version="           \$VER: AudioScope.sh_Version_0.00.70_PD_B.Walker_G0LCU.           "
setup=" Please wait while the very first scan and configuration file is generated. "
# Default first time run capture mode, 0 = DEMO.
demo=0
# Draw proceedure mode, 0 = OFF
drawline=0
# Pseudo-continuous data file saving.
savefile="0000000000"
save_string="OFF"
# "hold" and "status" will always be reset to "1" on program exit.
hold=1
status=1
# "count", "number" and "char" are reusable variables...
count=0
number=0
char="?"
# Vertical components...
# vert_one and vert_two are the vertical plotting points for the draw() function...
vert_one=2
vert_two=2
vert=12
vert_shift=2
vshift="?"
vert_array=""
vert_draw=9
# Display setup...
graticule="Public Domain, 2013, B.Walker, G0LCU."
# Keyboard components...
kbinput="?"
tbinput=1
# "str_len" is a reusable variable IF required...
str_len=1
# "grab" is used for internal pseudo-synchronisation...
grab=0
# "zero_offset" can only be manually changed in the AudioScope.config file, OR, here...
zero_offset=-2
# Horizontal components...
horiz=9
# Scan retraces...
scan=1
scanloops=1
# Timebase variable components...
subscript=0
# "scan_start" is from 0 to ( length of file - 64 )...
scan_start=0
# "scan_jump" is from 1 to ( ( ( scan_end - scan_start ) / 64) + 1 )...
scan_jump=1
# "scan_end" is at least 64 bytes in from the absolute file end...
scan_end=47935
# Synchronisation variables...
# synchronise switches the syncchroisation ON or OFF...
synchronise="OFF"
# sync_point is any value between 15 and 240 of the REAL grab(s)...
sync_point=128
sync_input="?"

# #########################################################
# Add the program tilte to the Terminal title bar...
# This may NOT work in every Terminal so just comment it out if it doesn't.
printf "\x1B]0;Shell AudioScope.\x07"

# #########################################################
# Generate a config file and temporarily store inside /tmp
if [ -f /tmp/AudioScope.config ]
then
	. /tmp/AudioScope.config
else
	user_config
fi
user_config()
{
	> /tmp/AudioScope.config
	chmod 644 /tmp/AudioScope.config
	printf "demo=$demo\n" >> /tmp/AudioScope.config
	printf "drawline=$drawline\n" >> /tmp/AudioScope.config
	printf "hold=1\n" >> /tmp/AudioScope.config
	printf "status=1\n" >> /tmp/AudioScope.config
	printf "zero_offset=$zero_offset\n" >> /tmp/AudioScope.config
	printf "scanloops=$scanloops\n" >> /tmp/AudioScope.config
	printf "scan_start=$scan_start\n" >> /tmp/AudioScope.config
	printf "scan_jump=$scan_jump\n" >> /tmp/AudioScope.config
	printf "scan_end=$scan_end\n" >> /tmp/AudioScope.config
	printf "vert_shift=$vert_shift\n" >> /tmp/AudioScope.config
	printf "setup='$setup'\n" >> /tmp/AudioScope.config
	printf "save_string='$save_string'\n" >> /tmp/AudioScope.config
}

# #########################################################
# Screen display setup function.
display()
{
	# Set foregound and background graticule colours and foreground and background other window colours.
	printf "\x1B[0;36;44m"
	clear
	graticule="       +-------+-------+-------+---[\x1B[0;37;44mDISPLAY\x1B[0;36;44m]---+-------+-------+--------+       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       +-------+-------+-------+-------+-------+-------+-------+--------+ <     \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"     0 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+ <     \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       +-------+-------+-------+-------+-------+-------+-------+--------+ <     \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       |       |       |       |       +       |       |       |        |       \n"
	graticule=$graticule"       +-------+-------+-------+-------+-------+-------+-------+--------+       \n"
	graticule=$graticule" \x1B[0;37;40m+-----------------------------[COMMAND  WINDOW]------------------------------+\x1B[0;37;44m \n"
	graticule=$graticule" \x1B[0;37;40m| COMMAND:-                                                                  |\x1B[0;37;44m \n"
	graticule=$graticule" \x1B[0;37;40m+------------------------------[STATUS WINDOW]-------------------------------+\x1B[0;37;44m \n"
	graticule=$graticule" \x1B[0;37;40m| Stopped...                                                                 |\x1B[0;37;44m \n"
	graticule=$graticule" \x1B[0;37;40m|$setup|\x1B[0;37;44m \n"
	graticule=$graticule" \x1B[0;37;40m+----------------------------------------------------------------------------+\x1B[0;37;44m "  
	printf "$graticule"
	# Set the colours for plotting.
	printf "\x1B[1;37;44m"
}

# #########################################################
# Pick which method to capture, (and store), the waveform on the fly.
waveform()
{
	> /tmp/waveform.raw
	chmod 644 /tmp/waveform.raw
	# Demo mode, generate 48000 bytes of random data.
	if [ $demo -eq 0 ]
	then
		# Use "sleep" to simulate a 1 second burst.
		sleep 1
		# "/dev/urandom is now used instead of RANDOM as it is MUCH faster.
		dd if=/dev/urandom of=/tmp/waveform.raw bs=48000 count=1
	fi
	# Using the aging(/old) /dev/dsp device, mono, 8 bits per sample and 8KHz sampling rate, 8000 unsigned-integer bytes of data...
	# Now tested on PCLinuxOS 2009 and Debian 6.0.x.
	if [ $demo -eq 1 ]
	then
		# This uses the oss-compat installation from your distro's repository...
		dd if=/dev/dsp of=/tmp/waveform.raw bs=8000 count=1
	fi
	# The main means of obtaining the unsigned-integer data, using SoX, (Sound eXcahnge) from http://sox.sourceforge.net ...
	if [ $demo -eq 2 ]
	then
		# Change the absolute address for your location of "sox"...
		/Users/barrywalker/Downloads/sox-14.4.0/sox -q -V0 -d -t raw -r 48000 -b 8 -c 1 -e unsigned-integer -> /tmp/waveform.raw trim 0 00:01
	fi
}

# #########################################################
# Plot the points inside the window...
plot()
{
	subscript=$scan_start
	vert_array=""
	for horiz in {9..72}
	do
		vert=`hexdump -n1 -s$subscript -v -e '1/1 "%u"' /tmp/waveform.raw`
		# Add a small offset to give a straight line with zero input allowing for mid-point sound card bit error.
		vert=$[ ( $vert + $zero_offset ) ]
		if [ $vert -le 0 ]
		then
			vert=0
		fi
		if [ $vert -ge 255 ]
		then
			vert=255
		fi
		# Pseudo-vertical shift of + or - 1 vertical division maximum.
		vert=$[ ( ( $vert / 16 ) + $vert_shift ) ]
		# Ensure the plot is NOT out of bounds after moving the shift position.
		if [ $vert -le 2 ]
		then
			vert=2
		fi
		if [ $vert -ge 17 ]
		then
			vert=17
		fi
		subscript=$[ ( $subscript + $scan_jump ) ]
		# Generate a smple space delimited 64 sample array.
		vert_array="$vert_array$vert "
		printf "\x1B[1;37;44m\x1B["$vert";"$horiz"f*"
	done
	# Set end of plot to COMMAND window.
	printf "\x1B[0;37;40m\x1B[20;14f"
}

# #########################################################
# This function connects up the plotted points.
# Defaults to OFF on the very first time run and must be manually enabled if needed.
draw()
{
	statusline
	IFS=" "
	subscript=0
	number=0
	vert_one=2
	vert_two=2
	vert_draw=( $vert_array )
	for horiz in {9..71}
	do
		# Obtain the two vertical components.
		vert_one=${vert_draw[ $subscript ]}
		subscript=$[ ( $subscript + 1 ) ]
		vert_two=${vert_draw[ $subscript ]}
		# Now subtract them and obtain an absolute value - ALWAYS 0 to positive...
		number=$[ ( $vert_two - $vert_one ) ]
		number=${number#-}
		# This decision section _is_ needed.
		if [ $number -le 1 ]
		then
			: # NOP. Do nothing...
		fi
		# This section does the drawing...
		if [ $number -ge 2 ]
		then
			if [ $vert_one -gt $vert_two ]
			then
				vert_one=$[ ( $vert_one - 1 ) ]
				while [ $vert_one -gt $vert_two ]
				do
					printf "\x1B[1;37;44m\x1B["$vert_one";"$horiz"f*"
					vert_one=$[ $vert_one - 1 ]
				done
			fi
			if [ $vert_two -gt $vert_one ]
			then
				vert_one=$[ ( $vert_one + 1 ) ]
				while [ $vert_one -lt $vert_two ]
				do
					printf "\x1B[1;37;44m\x1B["$vert_one";"$horiz"f*"
					vert_one=$[ $vert_one + 1 ]
				done
			fi

		fi
	IFS=$ifs_str
	done
	# Set end of plot to COMMAND window.
	printf "\x1B[0;37;40m\x1B[20;14f"
}

# #########################################################
# This is the information line _parser_...
statusline()
{
	printf "\x1B[0;37;40m\x1B[22;3f                                                                            \x1B[22;4f"
	if [ $status -eq 0 ]
	then
		printf "Stopped..."
	fi
	if [ $status -eq 1 ]
	then
		printf "Running $scan of $scanloops scans..."
	fi
	if [ $status -eq 2 ]
	then
		printf "Running in single shot storage mode..."
	fi
	if [ $status -eq 3 ]
	then
		printf "Drawing the scan..."
	fi
	if [ $status -eq 4 ]
	then
		printf "Synchroniastion set to $sync_point$synchronise..."
	fi
	if [ $status -eq 5 ]
	then
		printf "CAUTION, AUTO-SAVING FACILITY ENABLED!!!"
	fi
	if [ $status -eq 254 ]
	then
		status=1
		setup=$version
		printf "\x1B[23;3f$setup"
	fi
	# Set end of plot to COMMAND window.
	printf "\x1B[0;37;40m\x1B[20;14f"
}

# #########################################################
# All keyboard commands appear here when the scanning stops; there will be lots of them to make subtle changes...
kbcommands()
{
	IFS=$ifs_str
	status=1
	scan=1
	read -p "Press <CR> to (re)run, HELP or QUIT<CR> " -e kbinput
	printf "\x1B[0;37;40m\x1B[20;14f                                                                 "
	# Rerun scans captured or stored.
	if [ "$kbinput" == "" ]
	then
		status=1
		statusline
	fi
	# Run scans in captured, (REAL scan), mode only.
	if [ "$kbinput" == "RUN" ]
	then
		status=1
		hold=1
		statusline
	fi
	# Swtich off capture mode and rerun one storage shot only, this disables the DRAW command.
	# Use DRAW to re-enable again. This is deliberate for slow machines...
	if [ "$kbinput" == "HOLD" ]
	then
		drawline=0
		status=2
		hold=0
		scanloops=1
		statusline
		sleep 1
	fi
	# Quit the program.
	if [ "$kbinput" == "QUIT" ]
	then
		status=255
		break
	fi
	# Display the _online_ HELP file in default terminal colours.
	if [ "$kbinput" == "HELP" ]
	then
		status=0
		scanloops=1
		hold=0
		commandhelp
	fi
	# Enable DEMO pseudo-capture mode, default, but with 10 sweeps...
	if [ "$kbinput" == "DEMO" ]
	then
		status=1
		scan_start=0
		scan_jump=1
		scanloops=10
		scan_end=47935
		demo=0
		hold=1
		statusline
		sleep 1
	fi
	# Enable /dev/dsp capture mode, if your Linux flavour does NOT have it, install oss-compat from the distro's repository.
	# This is the mode used to test on Debian 6.0.x and now PCLinuxOS 2009...
	if [ "$kbinput" == "DSP" ]
	then
		status=1
		scan_start=0
		scan_jump=1
		scanloops=1
		scan_end=7935
		hold=1
		demo=1
		statusline
		sleep 1
	fi
	# Eable SOX capture mode, this code is designed around this application on a Macbook Pro 13 inch OSX 10.7.5...
	if [ "$kbinput" == "SOX" ]
	then
		status=1
		scan_start=0
		scan_jump=1
		scanloops=1
		scan_end=47935
		hold=1
		demo=2
		statusline
		sleep 1
	fi
	# The next three commands set the timebase scans; 1, 10 or 100 before COMMAND mode is re-enabled and can be used.
	if [ "$kbinput" == "ONE" ]
	then
		status=1
		scanloops=1
		hold=1
	fi
	if [ "$kbinput" == "TEN" ]
	then
		status=1
		scanloops=10
		hold=1
	fi
	if [ "$kbinput" == "HUNDRED" ]
	then
		status=1
		scanloops=100
		hold=1
	fi
	if [ "$kbinput" == "VER" ]
	then
		status=254
	fi
	# ************ Horizontal components. *************
	# ************ User timebase section. *************
	# Written longhand for kids to understand.
	if [ "$kbinput" == "TBVAR" ]
	then
		# Ensure capture mode is turned off.
		# RUN<CR> will re-enable it if required.
		scanloops=1
		status=1
		hold=0
		printf "\x1B[0;37;40m\x1B[20;14f"
		read -p "Set timebase starting point. From 0 to $scan_end<CR> " -e tbinput
		printf "\x1B[0;37;40m\x1B[20;14f                                                                 \x1B[0;37;40m\x1B[20;14f"
		# Ensure the timebase values are set to default before changing.
		scan_start=0
		scan_jump=1
		# Eliminate any keyboard error longhand...
		# Ensure a NULL string does NOT exist.
		if [ "$tbinput" == "" ]
		then
			scan_start=0
			tbinput=0
		fi
		# Find the length of the inputted string.
		str_len=`printf "${#tbinput}"`
		# Set the string to the correct last position for the _subscript_ point.
		str_len=$[ ( $str_len - 1 ) ]
		# Now check for continuous numerical charaters ONLY.
		for count in $( seq 0 $str_len )
		do
			# Reuse variable _number_ to obtain each character per loop.
			number=`printf "${tbinput:$count:1}"`
			# Now convert the character to a decimal number.
			number=`printf "%d" \'$number`
			# IF ANY ASCII character exists that is not numerical then reset the scan start point.
			if [ $number -le 47 ]
			then
				scan_start=0
				tbinput=0
			fi
			if [ $number -ge 58 ]
			then
				scan_start=0
				tbinput=0
			fi
		done
		# If all is OK pass the "tbinput" value into the "scan_start" variable.
		scan_start=$tbinput
		# Do a final check that the number is not out of bounds.
		if [ $scan_start -le 0 ]
		then
			scan_start=0
		fi
		if [ $scan_start -ge $scan_end ]
		then
			scan_start=$scan_end
		fi
		# Use exactly the same method as above to determine the jump interval.
		# Now set the jump interval, this is the scan speed...
		printf "\x1B[0;37;40m\x1B[20;14f"
		read -p "Set timebase user speed. From 1 to $[ ( ( ( ( $scan_end - $scan_start ) / 64 ) + 1 ) ) ]<CR> " -e tbinput
		printf "\x1B[0;37;40m\x1B[20;14f                                                                 \x1B[0;37;40m\x1B[20;14f"
		# Eliminate any keyboard error longhand...
		# Ensure a NULL string does NOT exist.
		if [ "$tbinput" == "" ]
		then
			scan_jump=1
			tbinput=1
		fi
		# Find the length of the inputted string.
		str_len=`printf "${#tbinput}"`
		# Set the string to the correct last position for the _subscript_ point.
		str_len=$[ ( $str_len - 1 ) ]
		# Now check for continuous numerical charaters ONLY.
		for count in $( seq 0 $str_len )
		do
			# Reuse variable _number_ to obtain each character per loop.
			number=`printf "${tbinput:$count:1}"`
			# Now convert the character to a decimal number.
			number=`printf "%d" \'$number`
			# IF ANY ASCII character exists that is not numerical then reset the scan jump value.
			if [ $number -le 47 ]
			then
				scan_jump=1
				tbinput=1
			fi
			if [ $number -ge 58 ]
			then
				scan_jump=1
				tbinput=1
			fi
		done
		# If all is OK pass the "tbinput" value into the "scan_jump" variable.
		scan_jump=$tbinput
		# Do a final check that the number is not out of bounds.
		if [ $scan_jump -le 1 ]
		then
			scan_jump=1
		fi
		# Reuse number for upper limit...
		number=$[ ( ( ( $scan_end - $scan_start ) / 64 ) + 1 ) ]
		if [ $scan_jump -ge $number ]
		then
			scan_jump=$number
		fi
		printf "\x1B[0;37;40m\x1B[22;4fScan start at offset $scan_start, with a jump rate of $scan_jump."
		sleep 1
		setup=" Uncalibrated horizontal scan, vertical and storage modes, AC coupled only. "
	fi
	# ********** User timebase section end. ***********
	# ********* Calibrated timebase section. **********
	if [ "$kbinput" == "FASTEST" ]
	then
		scan_start=0
		scan_jump=1
		setup=" Uncalibrated horizontal scan, vertical and storage modes, AC coupled only. "
	fi
	if [ "$kbinput" == "1mS" ]
	then
		scan_start=0
		setup=" 1mS/DIV, uncalibrated vertical and storage modes, AC coupled only.         "
		if [ $demo -eq 0 ]
		then
			scan_jump=6
		fi
		if [ $demo -eq 1 ]
		then
			scan_jump=1
		fi
		if [ $demo -eq 2 ]
		then
			scan_jump=6
		fi
	fi
	if [ "$kbinput" == "10mS" ]
	then
		scan_start=0
		setup=" 10mS/DIV, uncalibrated vertical and storage modes, AC coupled only.        "
		if [ $demo -eq 0 ]
		then
			scan_jump=60
		fi
		if [ $demo -eq 1 ]
		then
			scan_jump=10
		fi
		if [ $demo -eq 2 ]
		then
			scan_jump=60
		fi
	fi
	if [ "$kbinput" == "100mS" ]
	then
		scan_start=0
		setup=" 100mS/DIV, uncalibrated vertical and storage modes, AC coupled only.       "
		if [ $demo -eq 0 ]
		then
			scan_jump=600
		fi
		if [ $demo -eq 1 ]
		then
			scan_jump=100
		fi
		if [ $demo -eq 2 ]
		then
			scan_jump=600
		fi
	fi
	# *********** Calibrated timebase end. ************
	#
	# ************* Vertical components. **************
	# ******** Pseudo-vertical shift control. *********
	if [ "$kbinput" == "SHIFT" ]
	then
		while true
		do
			scanloops=1
			status=1
			hold=0
			printf "\x1B[0;37;40m\x1B[20;14f"
			# This input method is something akin to BASIC's INKEY$...
			read -p "Vertical shift:- U for up 1, D for down 1, <CR> to RETURN:- " -n 1 -s vshift
			printf "\x1B[0;37;40m\x1B[20;14f                                                                 \x1B[0;37;40m\x1B[20;14f"
			if [ "$vshift" == "" ]
			then
				break
			fi
			if [ "$vshift" == "D" ]
			then
				vert_shift=$[ ( $vert_shift + 1 ) ]
			fi
			if [ "$vshift" == "U" ]
			then
				vert_shift=$[ ( $vert_shift - 1 ) ]
			# Ensure the shift psoition is NOT out of bounds.
			fi
			if [ $vert_shift -ge 6 ]
			then
				vert_shift=6
			fi
			if [ $vert_shift -le -2 ]
			then
				vert_shift=-2
			fi
			printf "\x1B[23;3f Vertical shift is $[ ( 2 - $vert_shift ) ] from the mid-point position...                        "
		done
	fi
	# ****** Pseudo-vertical shift control end. *******
	# ********** Connect all plotted points. **********
	if [ "$kbinput" == "DRAW" ]
	then
		drawline=1
		status=3
		hold=0
		scanloops=1
		statusline
		sleep 1
	fi
	# ************* Connected plots done. *************
	#
	# **** PSEUDO synchronisation and triggering. ****
	if [ "$kbinput" == "TRIG" ]
	then
		synchronise=" and OFF"
		sync_point=128
		status=0
		hold=0
		scan_start=$[ ( $scan_start + 1 ) ]
		scan_jump=1
		scanloops=1
		subscript=$scan_start
		grab=0
		if [ $scan_start -ge $scan_end ]
		then
			scan_start=0
			break
		fi
		printf "\x1B[0;37;40m\x1B[20;14f"
		read -p "Set trigger type, <CR> to disable:- " -e kbinput
		printf "\x1B[0;37;40m\x1B[20;14f                                                                 \x1B[0;37;40m\x1B[20;14f"
		if [ "$kbinput" == "SYNCEQ" ]
		then
			synchronise=", ON and fixed"
			trigger
			for subscript in $( seq $scan_start $scan_end )
			do
				grab=`hexdump -n1 -s$subscript -v -e '1/1 "%u"' /tmp/waveform.raw`
				if [ $grab -eq $sync_point ]
				then
					scan_start=$subscript
					break
				fi
			done
		fi
		if [ "$kbinput" == "SYNCGT" ]
		then
			synchronise=", ON and positive going"
			trigger
			: # NOP... Place holder only.
		fi
		if [ "$kbinput" == "SYNCLT" ]
		then
			synchronise=", ON and negative going"
			trigger
			: # NOP... Place holder only...
		fi
		if [ "$kbinput" == "EXT" ]
		then
			# Remember Corona688's code from the early stages of this thread...
			synchronise=", EXTERNAL and waiting"
			: # NOP... Place holder only,
		fi
		status=4
		statusline
		sleep 1
	fi
	# ** PSEUDO synchronisation and triggering end. ***
	#
	# ************* Auto-saving facility. *************
	if [ "$kbinput" == "SAVEON" ]
	then
		status=5
		save_string="ON"
		statusline
		sleep 2
	fi
	if [ "$kbinput" == "SAVEOFF" ]
	then
		status=1
		save_string="OFF"
		statusline
	fi
	# *********** Auto-saving facility end. ***********
	statusline
}

# #########################################################
# Help clears the screen to the startup defaults and prints command line help...
commandhelp()
{
	status=2
	hold=0
	printf "\x1B[0m"
	clear
	printf "CURRENT COMMANDS AVAILABLE:-\n\n"
	printf "<CR> ................................................. Reruns the scan(s) again.\n"
	printf "RUN<CR> ......................... Reruns the scan(s), always with real captures.\n"
	printf "QUIT<CR> .................................................... Quits the program.\n"
	printf "HELP<CR> ................................................ This help as required.\n"
	printf "HOLD<CR> ........................................ Switch to pseudo-storage mode.\n"
	printf "DEMO<CR> .......... Switch capture to default DEMO mode and 10 continuous scans.\n"
	printf "DSP<CR> ...................... Switch capture to Linux /dev/dsp mode and 1 scan.\n"
	printf "SOX<CR> ....... Switch capture to multi-platform SOund eXchange mode and 1 scan.\n"
	printf "ONE<CR> ......................................... Sets the number of scans to 1.\n"
	printf "TEN<CR> ........................................ Sets the number of scans to 10.\n"
	printf "HUNDRED<CR> ............. Sets the number of scans to 100, (not very practical).\n"
	printf "VER<CR> .................. Displays the version number inside the status window.\n"
	printf "TBVAR<CR> ............ Set up uncalibrated user timebase offset and jump points.\n"
	printf "        SubCommands: ............................. Follow the on screen prompts.\n"
	printf "FASTEST<CR> .................. Set all modes to the fastest possible scan speed.\n"
	printf "1mS<CR> .......................................... Set scanning rate to 1mS/DIV.\n"
	printf "10mS<CR> ........................................ Set scanning rate to 10mS/DIV.\n"
	printf "100mS<CR> ...................................... Set scanning rate to 100mS/DIV.\n"
	printf "SHIFT<CR> ............ Set the vertical position from -4 to +4 to the mid-point.\n"
	printf "        SubCommands: ............ Press U or D then <CR> when value is obtained.\n"
	printf "\n"
	read -p "Press <CR> to continue:- " -e kbinput
	clear
	printf "CURRENT COMMANDS AVAILABLE:-\n\n"
	printf "DRAW<CR> .......... Connect up each vertical plot to give a fully lined display.\n"
	printf "TRIG<CR> ........... Sets the synchronisation methods for storage mode retraces.\n"
	printf "        SubCommand: SYNCEQ ........ Set the internal SYNC to a fixed value only.\n"
	printf "        SubCommand: SYNCGT ......................................... Unfinished.\n"
	printf "        SubCommand: SYNCLT ......................................... Unfinished.\n"
	printf "        SubCommand: EXT ............................................ Unfinished.\n"
	printf "SAVEON<CR> .................... Auto-saves EVERY scan with a numerical filename.\n"
	printf "SAVEOFF<CR> ....................................... Disables auto-save facility.\n"
	printf "\n"
	printf "Manual here: <  http://wisecracker.host22.com/public/AudioScope_Manual.readme  >\n"
	printf "\n"
	read -p "Press <CR> to continue:- " -e kbinput
	display
	statusline
}

# #########################################################
# This is the active part of the pseudo-synchroisation section.
trigger()
{
	while true
	do
		printf "\x1B[0;37;40m\x1B[20;14f"
		# This input method is something akin to BASIC's INKEY$...
		read -p "Sync point:- U for up 1, D for down 1, <CR> to RETURN:- " -n 1 -s sync_input
		printf "\x1B[0;37;40m\x1B[20;14f                                                                 \x1B[0;37;40m\x1B[20;14f"
		if [ "$sync_input" == "" ]
		then
			break
		fi
		if [ "$sync_input" == "U" ]
		then
			sync_point=$[ ( $sync_point + 1 ) ]
		fi
		if [ "$sync_input" == "D" ]
		then
			sync_point=$[ ( $sync_point - 1 ) ]
		# Ensure the synchronisation point is NOT out of bounds.
		fi
		if [ $sync_point -ge 240 ]
		then
			sync_point=240
		fi
		if [ $sync_point -le 15 ]
		then
			sync_point=15
		fi
		printf "\x1B[23;3f Synchronisation point set to $sync_point...                                        "
	done
}

# #########################################################
# Do an initial screen set up...
display
statusline
setup=$version

# #########################################################
# This is the main loop...
while true
do
	for scan in $( seq 1 $scanloops )
	do
		# "hold" determines a new captured scan or retrace of an existing scan...
		if [ $hold -eq 1 ]
		then
			waveform
		fi
		display
		statusline
		plot
		if [ $drawline -eq 1 ]
		then
			draw
		fi
		if [ "$save_string" == "ON" ]
		then
			savefile=`date +%s`
			cp /tmp/waveform.raw /tmp/$savefile
		fi
	done
	status=0
	statusline
	kbcommands
done

# #########################################################
# Getout, autosave AudioScope.config, cleanup and quit...
if [ $status -eq 255 ]
then
	# Save the user configuration file.
	user_config
	# Remove "Shell AudioScope" from the title bar.
	printf "\x1B]0;\x07"
	sleep 0.1
	# Reset back to normal...
	printf "\x1B[0m"
	clear
	reset
fi
printf "\nProgram terminated...\n\nTerminal reset back to startup defaults...\n\n"

# #########################################################
# The FIRST extremely simple construction part.
# This is a simple I/O board for testing for the Macbook Pro 13 inch...
# It is just as easy to replace the 4 pole 3.5mm Jack Plug with 2 x 3.5mm Stereo Jack
# Plugs for machines with separate I/O sockets.
#                                                       Orange.       White flylead.
# Tip ----->  O  <------------------------------------+---------O <----------+--------+
# Ring 1 -->  H  <-------------------------+-----------)--------O <- Blue.   |        |
# Ring 2 -->  H  <--------------+-----+-----)----------)--------O <- Yellow. |        |
# _Gnd_ --->  H  <----+         |  C1 | +  |          |         O <- Green.  |        |
#           +===+     |         \   =====  \          \         |            \        |
#           |   |     |         /   --+--  /          /         |            /        |
#        P1 |   |     |         \     |    \          \         |            \        |
#           |   |     |      R1 /     | R2 /       R3 /         |         R4 /        |
#            \ /      |         \     |    \          \         |            \        |
#             H       |         /     |    /          /         |            /        |
#            ~~~      |         |     |    |          |         |            |        |
#                     +---------+------)---+----------+---------+------------+        |
# Pseudo-Ground. -> __|__             |                                               |
#                   /////             +-----------------------------------------------+
# P1 ......... 3.5mm, 4 pole jack plug.
# R1 ......... 2K2, 1/8W, 5% tolerence resistor.
# R2, R3 ..... 33R, 1/8W, 5% tolerence resistor.
# R4 ......... 1M, 1/8W, 5% tolerence resistor.
# C1 ......... 47uF, 16V electrolytic.
# 4 way terminal block.
# Stripboard, (Verobaord), as required.
# Green, yellow, orange, blue and white wire as required.
# Small cable ties, optional.
# Stick on cable clip, optional.
# Crimp terminal, 1 off, optional.
# #########################################################
