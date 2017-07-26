#-------------------------------------------------------------------------------
#	Track Debug Package		argument(s) are option(s) and/or a debug message to be saved to a file
#	Usage:
#		package require tracks
#		pTrack ?-on? ?-off? ?-clear? ?-overflow? ?-overflowGo? ?-abend? ?"104 message text"?
#
#		A user-specified text message is written to a file "tracklst.txt" in the same directory
#		as the source program. Tracking can be turned on or off, and the clear option sets the
#		file to zero bytes. The program defaults to raise an error if the tracklst.txt file
#		gets too big (default is one megabyte), but the overflowGo option will cause it to just
#		turn off tracking and continue. The abend option will raise an optional error. The
#		message is whatever the user wants it to be, but suggested usage is to always start
#		with three digits that identify a proc and a fourth alphabetic character that marks
#		the track uniquely and allows searching for a specific track.
#
#		e.g.:  pTrack -clear "Start a new test by emptying the track file"
#		       pTrack "140d date adjusted to $tMon of $tYear"
#		       pTrack "135b Current working directory is [pwd]"
#
#------------------------------------------------------------------------------

	package provide tracks 1.0

namespace eval tracks {								;# define the tracks namespace:
	namespace export  pTrack  pDisplay				;#   export pTrack and pDisplay debug tools
	variable bTrackFlag On							;#   tracking on/off flag
	variable nOverflow 1000000						;#   max size of track file before turnoff is triggered
	variable bOverflowGo 0							;#   if file size is exceeded, if true, continue the program
	variable bSilentDisplay Off						;#   pDisplay is in silent mode (no displays wanted)
} ;# end namespace tracks


proc pTrack { args } {								;# write debug text to a debug log file
	if { $tracks::bTrackFlag == Off }  {			;# if tracking is turned off
		return "tracking turned off"				;#   go back to caller
	}
	if {$tracks::bTrackFlag==""} {					;# if track flag is empty
		set tracks::bTrackFlag On					;#   turn the track flag on
	}
	if {[llength $args] < 1} {
		return "no args"
	}
	set sMsg ""										;# initialize the debug message
	set bAbend Off									;# initialize the abend flag
	set bOption Off									;# initialize the option flag

#	pTrack ?-on? ?-off? ?-clear? ?-overflow=99999? ?-overflowGo? ?-abend? ?"104 message text"?	;# handle -options:

	foreach sItem [lrange $args 0 end] {			;#   for each arg in the track arguments
		#pDisplay "next item is <$sItem>"
		if { [string range $sItem 0 0] == "-" } {	;# if item starts with a hyphen ('-')
			set sItem [string tolower $sItem]		;#     convert arg to lower case
			set bOption On							;#     set the option flag
			#pDisplay "next item is<$sItem> (case adjusted)"
		}
		if {[string range $sItem 0 9] == "-overflow=" } {	;#   if -overflow option
			#pDisplay "overflow recognized in: <$sItem>"
			set n [string range $sItem 10 end]		;#     get the number
			#pDisplay "overflow number is <$n>"

			set m [split $n ".,b'"]					;# strip the commas etc out of the overflow number
			#pDisplay "m=<$m> a list without commas"
			set n [join $m ""]
			#pDisplay "n=<$n> a string integer without punctuation"

			if { [string length $n] > 8 } {			;# if overflow has too many digits
				set n "x"							;#   kill the overflow value so it will be rejected
				set sItem " + <$sItem> ignored, max is 8 digits + "	;#   error message
			}

			if {[ string is integer -strict $n ]} {	;# if overflow is an integer (else error, ignore the number)
				set tracks::nOverflow $n			;# set max file size to the integer
				#pDisplay "$tracks::nOverflow=<$n>--overflow set"
				continue							;# continue with the next foreach loop iteration
			}
		}
		switch $sItem {
			-abend {
				set sMsg "$sMsg + $sItem "			;# accumulate the abend message
				set bAbend On						;# set the abend flag on
			}
			-clear {
				set hFile1 [open "tracklst.txt" w]	;#   open for write (will clear the file)
				close $hFile1						;#   close the file
			}
			-off {
				set tracks::bTrackFlag Off			;#   turn the track flag off
			}
			-on {
				set tracks::bTrackFlag On			;#   turn the track flag on
			}
			-overflowGo {
				set tracks::bOverflowGo 1			;#   turn the track overflow-continue flag on
			}
			default {
				set sMsg "$sMsg $sItem "		;# accumulate the message (all non-option stuff is concatenated)
			}
		}
	}

	set now [clock seconds]							;# get the current time for a timestamp
	set sTrkTimeStamp [clock format $now -format "%Y/%m/%d-%k:%M:%S>"]	;# format the timestamp into the track message
	set hFile1 [open "tracklst.txt" a]				;# open the track file

	if { $tracks::bTrackFlag == "On" || $bOption } {  ;# if track flag is on or options are specified
		puts $hFile1 "$sTrkTimeStamp Track: <$sMsg>" ;#   append track message to track file
	}

	if { $bAbend eq On } {							;# if abend flag is ON
		close $hFile1								;#   close the track file
		error "ABEND TR1002: pTrack caller has chosen to raise an error" ;# rais an error
		pDisplay "9998 after the error abend line"
		exit										;#   quit
		pDisplay "9998 after the exit abend line"
	}

	set nSize [file size "tracklst.txt"]			;# get the track file size
	if { $nSize > $tracks::nOverflow } {			;# if track file is too big      OVERFLOW ERROR!
		set sOverflowMessage "Track File Overflow Error. Tracking has been turned off (pTrack is choosing to raise an error \
			because the track file is too big (tracklst.txt is [pTracksCommify $nSize] characters long)"
		puts $hFile1 "$sTrkTimeStamp Track: 999x <$sOverflowMessage>"	;# append text to track file
		set tracks::bTrackFlag Off					;# turn off tracking
		if { $tracks::bOverflowGo == 0 } {			;# if overflow continue has not been set
			puts $hFile1 "$sTrkTimeStamp Track: 999y Overflow Continue has NOT been specified, so program is exiting."
			close $hFile1							;#   close the track file
			exit 16									;#   exit to the system with a return code
		}
		set answer [tk_messageBox -message "pTrack File Overflow Error" \
			-icon question -type yesno \
			-detail "Tracking halted. Select \"YES\" to make the application exit, or NO to continue \
				(might be in an infinite loop)."]
		if {$answer == yes} {						;# if user wants to abort, end the program
			puts $hFile1 "$sTrkTimeStamp Track: 999z User chose EXIT option in dialog, so program is exiting"
			close $hFile1							;# close the track file
			exit 16									;#   exit to the system with a return code
		}
		puts $hFile1 "$sTrkTimeStamp Track: 999w Program is continuing with tracking turned off"
	}
	close $hFile1									;# close the track file
	return $tracks::bTrackFlag						;# go back to caller
} ;# end proc pTrack


#---------------------------------------------------------------------
#		Proc: pTracksCommify num sep
#	commify -- put commas into a decimal number
#	Arguments:		num		1000000		an integer
#					sep		,			separator char (defaults to English format ",")
#	Returns:		number	1,000,000	with commas in the appropriate places
#---------------------------------------------------------------------
proc pTracksCommify {num {sep ,}} {
	while {[regsub {^([-+]?\d+)(\d\d\d)} $num "\\1$sep\\2" num]} {}		;# the magic regexp
	return $num
} ;# end proc pTracksCommify


#---------------------------------------------------ppp---------------
#	Proc: pDisplay		show a debug message and handle responses
#---------------------------------------------------------------------
proc pDisplay { sMsg } {
	# display a debug message in a msgbox dialog with options "OK" "CANCEL" and "SILENT"
	# Arg:  sMsg  a debug text message line
	# Returns: "yes"  "no"  "cancel"

	if { $tracks::bSilentDisplay == On } {			;# if user has selected SILENT mode
		return 0									;#   just go back, no message wanted now
	}

	set sText "$sMsg\n\nContinue displaying pDisplay messages? (YES to continue, \
			NO to continue without pDisplay messages, or CANCEL to stop the program.)"
	set sAnswer [tk_messageBox -message $sText -default yes \
		-icon question  -type yesnocancel  -title "pDisplay Debug Message"]

	switch -- $sAnswer {
		no		{ set tracks::bSilentDisplay On }
		cancel	{ exit "User canceled in a pDisplay call."}
	}
	return 0										;# go back to the caller
} ;# end proc pDisplay
