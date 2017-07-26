# PROGRAM-NAME: VW.TCL              VERSION NO.: 1.01
# AUTHOR: Tony Dycks                REVISED-BY: Tony Dycks
# DATE-WRITTEN: August 7, 2001      DATE-REVISED: September 10, 2001
# LANGUAGE: Active State Tcl/Tk     VERSION. NO.: 8.3
# PLATFORMS TESTED: MS Windows 98/NT 4.0
#                   Red Hat Linux 7.1 / SuSE Linux 7.0
#
# DESCRIPTION:
#   Tcl/Tk Wish Script For Viewing A Text File Using A TK Window.
#   File Contents Are Displayed On Text Widget Using TK As A GUI.
#   A Scrollbar Widget Is Added To Allow The Viewing Of File Contents.
#   Program Uses A File Menu Options To Select Files For Viewing 
#   And To Exit The Program. Clicking The "Exit Program" Button Closes
#   The TK Window And Ends The Program. Bind To <F3> Function Key
#   To Exit The Program.
#
# USAGE:
#   WISH VW.TCL <Enter>
#     {Where WISH is a shell or bat file invoking the WISH executable}
#
# USAGE EXAMPLE:
#   WISH VW.TCL <Enter>  
#
# REFERENCES: 
#   Personal Derivation Of TCL/TK Code Using The Grid Layout Manager. 
#
# LICENSING: 
#   Released Under The GPL As Open Source. 
#
# +---------------------------------------------------+
# + Set Initial Directory To Current Logged Directory +
# +---------------------------------------------------+
set initialdir [pwd]
global initialdir
global flname
# +------------------------------------------------------+
# + Select Open Input Text File & Populate Entry Widgets +
# +------------------------------------------------------+
proc openfl {} {
  global initialdir
  global flname
  set file_types {
    {"Tcl Files" { .tcl .TCL } }
    {"Text Files" { .txt .TXT } }
    {"All Files"  * }
    }
# +-------------------------------------------------+
# + Cleanup Filename And Text File Contents Widgets +
# +-------------------------------------------------+
  .txtarea delete 1.0 end
  set flname [tk_getOpenFile -initialdir $initialdir     -filetypes $file_types -title "Open Input Text File" -parent .]
  if {$flname != ""} {
    set initialdir [file dirname $flname]
    set retcd [ catch { set infile [open $flname "r"] } ]
# +------------------------------------------------+
# + Display Error Message Box If File Open Failure +
# +------------------------------------------------+
    if {$retcd == 1} {
      wm title . "VW.TCL -- File Open Error Message"
      set result [tk_messageBox -parent .         -title "VW.TCL -- File Open Error Message" -type ok -icon error         -message         "Error Opening File: $flname.\n"]
      }
# +----------------------------------------------+
# + Open File Successful Load Text File Contents +
# + Line By Line Until End Of File               +
# +----------------------------------------------+
    if {$retcd == 0} {
      set inEOF -1
      set txln ""
      .txtarea delete 1.0 end
      while {[gets $infile inln] != $inEOF} {
        set txln "$inln\n"
        .txtarea insert end $txln
        }
      close $infile
      }
    }
  return $flname
  }
# +------------------+
# + Exit The Program +
# +------------------+
proc exitpgm {} {
  exit 0
  }

# +-------------------------------------------------+
# + Initial TK Widget Definitions For Viewer Window +
# +-------------------------------------------------+
wm title . "VW.TCL Version 1.01 -- Text File Viewer Tcl/Tk Progam"
# +--------------+
# + Menu Widgets +
# +--------------+
menubutton .fl -text "File" -menu .fl.menu -anchor nw
menu .fl.menu
.fl.menu add command -label "Open" -command openfl
.fl.menu add separator
.fl.menu add command -label "Exit" -command exitpgm
set font {Verdana 14}
# +------------------------+
# + Filename Label Widgets +
# +------------------------+
label .fllabel -text "Input Filename:" -relief sunken -bg NavajoWhite2   -fg Navy -anchor nw
label .flname -width 80 -relief sunken -bg NavajoWhite2   -fg Navy -textvariable flname -anchor nw
pack .fl .fllabel .flname -side top -padx 1m -pady 1m -anchor nw
# +----------------------------------------+
# + Text File Contents & Scrollbar Widgets +
# +----------------------------------------+
label .fltext -width 80 -relief sunken -bg White -textvariable fltext
text .txtarea -bg LightYellow2 -font FixedSys -bd 2   -yscrollcommand ".vscroller set"
scrollbar .vscroller -command ".txtarea yview"
pack .txtarea .vscroller -side left -fill y
# +-----------------------------------------------------+
# + Command Button Widgets For Open File & Program Exit +
# +-----------------------------------------------------+
button .openfl -text "<< Open File >>" -fg Navy -bg NavajoWhite2   -font bold -command openfl
button .exitpgm -text "< Exit Program >" -fg Navy -bg NavajoWhite2   -font bold -command exitpgm
pack .exitpgm .openfl -side bottom -padx 1m -pady 1m 

bind .txtarea <Key-F3> {exitpgm}
bind .fllabel <Key-F3> {exitpgm}
bind .flname <Key-F3> {exitpgm}
