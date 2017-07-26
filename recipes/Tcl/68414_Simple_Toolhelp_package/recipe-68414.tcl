# poToolhelp.tcl
# Simple package to implement a toolhelp widget.
# Paul Obermeier, 2001.

package provide poToolhelp 1.0

namespace eval ::poToolhelp {
    namespace export AddBinding
    namespace export Init

    variable topWidget
}

proc ::poToolhelp::Init { w { bgColor lightyellow } { fgColor black } } {
    variable topWidget

    # Create Toolbar help window with a simple label in it.
    if { [winfo exists $w] } {
	destroy $w
    }
    toplevel $w
    set topWidget $w
    label $w.l -text "This is toolhelp" -bg $bgColor -fg $fgColor -relief ridge
    pack $w.l
    wm overrideredirect $w true
    wm geometry $w [format "+%d+%d" -100 -100]
}

proc ::poToolhelp::ShowToolhelp { x y str } {
    variable topWidget

    $topWidget.l configure -text $str
    raise $topWidget
    wm geometry $topWidget [format "+%d+%d" $x [expr $y +10]]
}

proc ::poToolhelp::HideToolhelp {} {
    variable topWidget

    wm geometry $topWidget [format "+%d+%d" -100 -100]
}

proc ::poToolhelp::AddBinding { w str } {
    variable topWidget

    if { ![info exists topWidget]} {
	Init .poToolhelp
    }
    bind $w <Enter>  "::poToolhelp::ShowToolhelp %X %Y [list $str]"
    bind $w <Leave>  "::poToolhelp::HideToolhelp"
    bind $w <Button> "::poToolhelp::HideToolhelp"
}

catch {puts "Loaded Package poToolhelp (File [info script])"}

# Demo code. Uncomment for testing.

# package require poToolhelp

# pack [button .b -text "This is a button"] -fill x -expand 1
# ::poToolhelp::AddBinding .b "Toolhelp for a button"
# pack [label .l -text "This is a label"] -fill x -expand 1
# ::poToolhelp::AddBinding .l "Toolhelp for a label"
# set eVar "This is a entry"
# pack [entry .e -textvariable eVar] -fill x -expand 1
# ::poToolhelp::AddBinding .e "Toolhelp for a entry"
# pack [button .q -text "Quit" -command exit] -fill x -expand 1
# ::poToolhelp::AddBinding .q "Really want to quit this fabulous program ?"
