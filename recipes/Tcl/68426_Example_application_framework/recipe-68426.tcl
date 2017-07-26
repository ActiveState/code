# poAppFrame.tcl
# Example application framework.
# Needs packages poToolhelp and poToolbar.
# Paul Obermeier, 2001.

catch {console show}
set auto_path [linsert $auto_path 0 [file dirname [info script]]]

package require poToolhelp
package require poToolbar

proc NewBmp {} {
    return {
    #define newfile_width 16
    #define newfile_height 16
    static unsigned char newfile_bits[] = {
       0x00, 0x00, 0x00, 0x00, 0xfc, 0x03, 0x04, 0x06, 0x04, 0x0a, 0x04, 0x1e,
       0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10,
       0x04, 0x10, 0x04, 0x10, 0xfc, 0x1f, 0x00, 0x00};
    }
} 

proc OpenBmp {} {
    return {
    #define open_width 16
    #define open_height 16
    static unsigned char open_bits[] = {
       0x00, 0x00, 0x00, 0x0e, 0x00, 0x51, 0x00, 0x60, 0x0e, 0x70, 0xf1, 0x07,
       0x01, 0x04, 0x01, 0x04, 0xe1, 0xff, 0x11, 0x40, 0x09, 0x20, 0x05, 0x10,
       0x03, 0x08, 0xff, 0x07, 0x00, 0x00, 0x00, 0x00};
    }
}

proc SaveBmp {} {
    return {
    #define save_width 16
    #define save_height 16
    static unsigned char save_bits[] = {
       0x00, 0x00, 0xfe, 0x7f, 0x0a, 0x50, 0x0a, 0x70, 0x0e, 0x50, 0x0e, 0x50,
       0x0e, 0x50, 0x0a, 0x50, 0xf2, 0x4f, 0x02, 0x40, 0xf2, 0x5f, 0xf2, 0x53,
       0xf2, 0x53, 0xf2, 0x53, 0xfc, 0x7f, 0x00, 0x00};
    }
}

proc NewProc {} {
    WriteInfoStr "You selected NewProc"
}

proc OpenProc {} {
    WriteInfoStr "You selected OpenProc"
}

proc SaveProc {} {
    WriteInfoStr "You selected SaveProc"
}

proc HelpProc {} {
    tk_messageBox -title "Help window" 	 \
           -message "Tcl/Tk application framework written by Paul Obermeier" \
	   -type ok -icon info
    focus .
}

proc AddMenuCmd { menu label acc cmd } {
    $menu add command -label $label -accelerator $acc -command $cmd
}

proc WriteInfoStr { str } {
    .fr.infofr.l configure -text $str
}

set hMenu .menufr
menu $hMenu -borderwidth 2 -relief sunken
$hMenu add cascade -menu $hMenu.file -label File -underline 0
$hMenu add cascade -menu $hMenu.help -label Help -underline 0

set fileMenu $hMenu.file
menu $fileMenu -tearoff 0

AddMenuCmd $fileMenu "New ..."     "Ctrl+N" NewProc
AddMenuCmd $fileMenu "Open ..."    "Ctrl+O" OpenProc
AddMenuCmd $fileMenu "Save ..."    "Ctrl+S" SaveProc
AddMenuCmd $fileMenu "Quit ..."    "Ctrl+Q" exit
bind . <Control-n> NewProc
bind . <Control-o> OpenProc
bind . <Control-s> SaveProc
bind . <Control-q> exit

set helpMenu $hMenu.help
menu $helpMenu -tearoff 0
AddMenuCmd $helpMenu "About ..."   "F1" HelpProc
bind . <F1> HelpProc

wm protocol . WM_DELETE_WINDOW "exit"
. configure -menu $hMenu

frame .fr
pack .fr -fill both -expand 1

frame .fr.toolfr -relief sunken -borderwidth 1
frame .fr.workfr -relief sunken -borderwidth 1 -bg green
frame .fr.infofr -relief sunken -borderwidth 1
grid .fr.toolfr -row 0 -column 0 -sticky ew
grid .fr.workfr -row 1 -column 0 -sticky news
grid .fr.infofr -row 2 -column 0 -sticky ew
grid rowconfigure    .fr 1 -weight 1
grid columnconfigure .fr 0 -weight 1

label .fr.infofr.l -text "Info widget"
pack .fr.infofr.l -fill both -expand 1

label .fr.workfr.l \
       -text "This is the working frame for your widgets"  \
       -bg green
pack .fr.workfr.l -fill x -expand 1

for {set grp 0} {$grp < 3} {incr grp} {
    set newGrp [::poToolbar::AddGroup .fr.toolfr]
    ::poToolbar::AddButton $newGrp.new [NewBmp] NewProc \
		       "New something (Ctrl+N)" -activebackground green
    ::poToolbar::AddButton $newGrp.open [OpenBmp] OpenProc \
		       "Open something (Ctrl+O)" -activebackground yellow
    ::poToolbar::AddButton $newGrp.save [SaveBmp] SaveProc \
		       "Save something (Ctrl+S)" -activebackground red
}
