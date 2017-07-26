#!/bin/sh
#the next line restarts using tclsh\
exec tclsh8.4 "$0" "$@"

set msg "is down"
set file "hostslist"
set hf [open $file r+ 440]
set glist [] 
foreach line [split [read $hf] \n]  {
	set ls [split $line :]
	lappend glist $ls 
}
close $hf
set fd [open logfile w+ 440]
puts $fd $glist
close $fd

proc connect {host port} {
global s
set s [socket $host $port]
}
proc alert { host res desc msg} {
puts "$host $res $desc $msg"
}
proc action {a} {
puts stdout [exec $a]
}

set n [llength $glist]
set n1 [llength [lindex $glist 0]]

for {set i 0 } {$i<[expr $n-1]} {incr i }  { 
set i1 0;set i2 [expr $n1-3];set i3 [expr $n1-2];set i4 [expr $n1-1] 
set host [lindex [lindex $glist $i] $i1]
set port [lindex [lindex $glist $i] $i2]
set act  [lindex [lindex $glist $i] $i3]
set desc [lindex [lindex $glist $i] $i4]
if {[catch {connect $host $port} result]} {
alert $host $result $desc $msg  
action $act
} else {
puts "$desc is ready"
  }
}
