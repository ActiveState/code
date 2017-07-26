# every --
#   Cheap rescheduler.  (c) Jeffrey Hobbs
#   
# every::schedule <time> cmd;	# cmd is a one arg (cmd as list)
#	schedules $cmd to be run every <time> 1000ths of a sec
#	IOW, [::every::schedule 1000 "puts hello"] prints hello every sec
# every::cancel pattern
#	cancels cmd matching the glob pattern
# every::info ?pattern?
#	returns info about commands in pairs of "time cmd time cmd ..."
#
namespace eval ::every {}
proc ::every::schedule {time cmd} {
    if {![string is integer -strict $time]} {
	return -code error "usage: [lindex [::info level 0] 0] time command"
    }
    # A time was given, so schedule a command to run every $time msecs
    variable ID
    if {[string compare {} $cmd]} {
	set ID($cmd) [list $time [after $time [list ::every::_do $cmd]]]
    }
}

proc ::every::_do {cmd} {
    variable ID
    if {[::info exists ID($cmd)]} {
	uplevel \#0 $cmd
	set time [lindex $ID($cmd) 0]
	set ID($cmd) [list $time [after $time [list ::every::_do $cmd]]]
    }
}

proc ::every::cancel {pattern} {
    variable ID
    foreach i [array names ID $pattern] {
	after cancel [lindex $ID($i) 1]
	unset ID($i)
    }
}

proc ::every::info {{pattern *}} {
    variable ID
    set result {}
    foreach i [array names ID $pattern] {
	lappend result [lindex $ID($i) 0] [lindex $ID($i) 1]
    }
    return $result
}
