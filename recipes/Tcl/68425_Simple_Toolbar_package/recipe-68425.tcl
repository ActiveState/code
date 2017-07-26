# poToolbar.tcl
# Simple package to implement a toolbar.
# Paul Obermeier, 2001.

package provide poToolbar 1.0

namespace eval ::poToolbar {
    namespace export AddGroup
    namespace export AddButton
    namespace export AddCheckButton

    variable groupNum
}

proc ::poToolbar::Init {} {
    variable groupNum

    set groupNum 1
}

proc ::poToolbar::AddGroup { w } {
    variable groupNum

    if { ![info exists groupNum]} {
	Init
    }

    set newFrame $w.fr$groupNum
    frame $newFrame -relief raised -borderwidth 1
    pack  $newFrame -side left -fill y
    incr groupNum
    return $newFrame
}

proc ::poToolbar::AddButton { btnName bmpData cmd str args } {
    variable groupNum

    if { ![info exists groupNum]} {
	Init
    }

    if { [string compare $bmpData ""] == 0 } {
        eval button $btnName -relief flat -takefocus 0 \
                             -command [list $cmd] $args
    } else {
        set img [image create bitmap -data $bmpData]
        eval button $btnName -image $img -relief flat \
             -takefocus 0                              \
             -command [list $cmd] $args
    }
    ::poToolhelp::AddBinding $btnName $str
    pack $btnName -side left
}

proc ::poToolbar::AddCheckButton { btnName bmpData cmd str args } {
    variable groupNum

    if { ![info exists groupNum]} {
	Init
    }

    if { [string compare $bmpData ""] == 0 } {
        eval checkbutton $btnName -relief flat -indicatoron 0 \
  		         -takefocus 0 -command [list $cmd] $args
    } else {
        set img [image create bitmap -data $bmpData]
        eval checkbutton $btnName -image $img -relief flat -indicatoron 0 \
  		         -takefocus 0 -command [list $cmd] $args
    }
    ::poToolhelp::AddBinding $btnName $str
    pack $btnName -side left
}

catch {puts "Loaded Package poToolbar (File [info script])"}
