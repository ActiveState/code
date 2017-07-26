#!/bin/sh
# pass_gen - create pronouncable passwords with 4-20 characters, 1-10 numbers
#            and optional symbol
# author: Rob Haeusler
# licence: GPL
# tested on
#       puppy linux - initial development and testing
#	xubutu
#	windows xp
#
# changelog
# 1.1 - mods to allow different lengths of vowels, letters, digits, symbols
# 1.0 - initial development
#
#
#\
exec wish "$0" $(1+"$@")

# require following packages to operate
package require BWidget

set version "1.1"
set licence "G.P.L"

# data sets used for creating the password
set vowels { a e i o u }
set letters { b c d f g h j k l m n p q r s t v w x y z }
set digits { 0 1 2 3 4 5 6 7 8 9 }
set symbols { ! @ # $ % ^ & * ( ) _ - + }

# -----------------------------------------------------------------------------
# appCreate - create window frame and all its contents, spinboxes, buttons,
#             display elements
#
proc appCreate { } {

	# menu description
	set descmenu {
		"&File" all file 0 {
			{command "E&xit" {} "exit application" {} \
				-command appExit }
		}
	 	"&Help" all help 0 {
	       		{command "&About" {} "about the application" {} \
				-command appHelpAbout }
		}
	}

	# create the main menu
	wm title .  "pass_gen"
	set mainframe [MainFrame .mainframe -menu $descmenu ]

	# create spinboxes for number of letters and numbers
	set titf1 [TitleFrame $mainframe.titf1 -text "Number of Characters" ]
	set subf1 [$titf1 getframe]
	set spin1 [SpinBox $subf1.spin -range { 4 20 1 } -textvariable alpha ]

	pack $spin1 -side right
	pack $titf1 -fill x -pady 2 -padx 2

	set titf2 [TitleFrame $mainframe.titf2 -text "Number of Numbers" ]
	set subf2 [$titf2 getframe]
	set spin2 [SpinBox $subf2.spin -range { 1 10 1 } -textvariable numeric ]

	pack $spin2 -side right
	pack $titf2 -fill x -pady 2 -padx 2

	# create radio button  (yes/no choice) for symbols
	set titf3 [TitleFrame $mainframe.titf3 -text "Symbol"]
	set subf3 [$titf3 getframe]
	set rad1 [radiobutton $subf3.rad1 -text "Yes" \
			-variable wantsymbol -value 1]
	set rad2 [radiobutton $subf3.rad2 -text "No" \
			-variable wantsymbol -value 0]
	
	pack $rad1 $rad2 -side left
	pack $titf3 -fill x -pady 2 -padx 2

	# create display box for generated passwords
	set titf4 [TitleFrame $mainframe.titf4 -text "Password"]
	set subf4 [$titf4 getframe]
	set ent1 [Entry $subf4.entry -textvariable genpassword]

	pack $ent1 -pady 4 -anchor w -side left
	pack $titf4

	# create button for generating new password
	set but [Button $mainframe.but -text "New" \
		-command "newPass" -helptext "create new password" ]
	
	pack $but -side left -padx 4

	wm protocol . WM_DELETE_WINDOW { appExit }
	pack $mainframe -fill both -expand yes
	update idletasks
}

#
# newPass - determine how many letters, vowels, digits, symbols and display the
# created password
#
proc newPass { } {
	global genpassword alpha numeric wantsymbol

	set fpl [ expr $alpha / 2 ]

	if { $alpha % 2 } {
		set fpl [ expr int(alpha / 2) + 1]
	}

	set lpl [ expr $alpha - $fpl ]

	# to change format of password edit following lines
	set start [ aPart $fpl ]
	set mid [ nPart $numeric ]
	set end [aPart $lpl ]

	if { $wantsymbol == 1} {
		set sym [ sPart ]
		set genpassword [ format "%s%s%s%s" $start $mid $end $sym ]
	} else {
		set genpassword [format "%s%s%s" $start $mid $end ]
	}
}

#
# aPart - return randomly selected letters and vowels from the lists
#
proc aPart { slen } {
	global vowels letters

	set vlen [ expr [ llength $vowels ] - 1 ]
	set llen [ expr [ llength $letters ] - 1 ]

	for { set i 0 } { $i < $slen } { incr i } {
		if { $i % 2 == 0 } {
			set randid [ expr int( rand() * $llen ) ]
			append ret [ lindex $letters $randid ]
		} else {
			set randid [ expr int( rand() * $vlen ) ]
			append ret [ lindex $vowels $randid ]
		}
	}
	return $ret
}

#
# nPart - return randomly selected digit(s) from the digit list
#
proc nPart { slen } {
	global digits

	set dlen [ expr [ llength $digits] - 1 ]

	for { set i 0 } { $i < $slen } { incr i } {
		set randid [ expr int( rand() * $dlen ) ]
		append ret [ lindex $digits $randid ]
	}
	return $ret
}

#
# sPart - return randonly selected symbol from the list
#
proc sPart { } {
	global symbols

	set sylen [ expr [ llength $symbols ] - 1 ]
	set randid [ expr int( rand() * $sylen ) ]
	append ret [ lindex $symbols $randid ]
	return $ret
}

#
# appExit - selected from menu
#
proc appExit { } {
	exit
}

#
# appHelpAbout - display info about the program in new disposable window
#
proc appHelpAbout { } {
	global version licence

	tk_messageBox -message "Generate pronouncable passwords in form of \n\
        	- word, \n\
		- number, \n \
	        - word, \n \
		- optional symbol.\n\
		Author: Rob Haeusler.\n\
		Version: $version.\n\
		Licence: $licence."
}

#
# main procedure to manage window creation and destruction
#
proc main { } {
	wm withdraw .
	appCreate
	wm deiconify .
}

main
#---------------------------- end of program ----------------------------------
