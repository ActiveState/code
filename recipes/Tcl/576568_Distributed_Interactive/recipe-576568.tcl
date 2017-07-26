#!/bin/sh
# \
exec wish "$0" "$@"

# Decode Distributed Interactive Simulation (DIS) Protocol Data Units (PDUs) from UDP packets.
# written by Frank Bannon
# PDUs decoded: Entity State, Fire, Detonation, Transmitter, Signal
# written for TCL 8.4
# updated 2012.06.14

# http://tcludp.sourceforge.net
package require udp

set port 3000
set autoscroll 1

# does this platform use big-endian or little-endian floats?
# Author: kennykb@acm.org 
# http://groups.google.com/group/comp.lang.tcl/browse_thread/thread/adfc08a2709a634c
binary scan [binary format d 1.0] w test
switch -exact [format %16lx $test] { 
 3ff0000000000000 {set bigendian 0}
 0000000000000f3f {set bigendian 1}
 default {puts "machine does not have IEEE-754 support for floats"}
}

# workaround for TCL 8.4 having no big-endian binary format
proc cast_value {v vtype} {
global bigendian
switch -- $vtype {
 float {
	# convert float 64 bit to float
	if {$bigendian} {
		binary scan [binary format I $v] f v
	} else {
		binary scan [binary format i $v] f v
	}
	}
 long {
	# convert long 64 bit to long
	if {$bigendian} {
		binary scan [binary format W $v] d v
	} else {
		binary scan [binary format w $v] d v
	}
	}
 float64 {
	# convert float to 64 bit float
	if {$bigendian} {
		binary scan [binary format f $v] I v
	} else {
		binary scan [binary format f $v] i v
	}
	}
 long64 {
	# convert long to 64 bit long
	if {$bigendian} {
		binary scan [binary format d $v] W v
	} else {
		binary scan [binary format d $v] w v
	}
	}
}
return $v
}

proc log {str {tag ""}} {
global autoscroll
puts $str
# add to text widget if present
set w .f1.txt
if {[winfo exists $w]} {
	$w insert end "$str" $tag
	$w insert end "\n"
	if {$autoscroll} {$w yview end}
}
}

# return milliseconds from timestamp t
# added 2012.06.14
proc decode_timestamp {t} {
# right shift integer then compute ms
set absolutetime [expr $t & 1]
set ms [expr {int(($t >> 1) * (0.5 + 3600000.0) / 0x7fffffff)}]
set seconds [expr {int($ms / 1000)}]
if {$seconds < 0} {set seconds [expr {$seconds % 3600}]}
if {$absolutetime} {return [list $seconds absolute]}
return [list $seconds relative]
}

proc open_socket {port {multicast 0}} {
if {[catch {set s [udp_open $port -blocking 0]} result]} {
	return 0
}
fconfigure $s -blocking 0 -buffering none -translation binary
if {$multicast} {catch {fconfigure $s -mcastadd $multicast}}
fileevent $s readable [list read_socket $s]
log "connected to port $port using socket $s"
return $s
}

proc close_socket {sock} {
catch {close $sock}
}

proc read_socket {s} {
set pdu [read $s]
set d(kind) 0
# get PDU kind
if {[catch {binary scan $pdu ccc d(disver) d(exercise) d(kind)}]} {return}

# PARSE THE PDU
switch -- $d(kind) {
 1	{
	# ENTITY STATE PDU
	log "Entity State PDU"
	if {[catch {binary scan $pdu ccccISSSSSccccSccccccSccccIIIWWWIIIIcA39cA11I \
	d(disver) d(exercise) d(pdukind) d(family) d(time) d(length) pad \
	d(site) d(host) d(entity) d(force) d(articulations) \
	d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
	d(altkind) d(altdomain) d(altcountry) d(altcat) d(altsubcat) d(altspec) d(altextra) \
	d(velocityx) d(velocityy) d(velocityz) d(locationx) d(locationy) d(locationz) \
	d(orientx) d(orienty) d(orientz) \
	d(appearance) d(deadreckon) pad d(charset) d(marking) d(capabilities)} result]
	} {
		log $result
		return
	}
	# clean up data
	set d(time) [decode_timestamp $d(time)]
	# remove empty padding from marking field
	regsub -all {[[:cntrl:]]} $d(marking) { } d(marking)
	set d(marking) [string trim $d(marking)]
	# handle enum sometimes negative
	foreach v {cat subcat spec extra} {if {$d($v) < 0} {incr d($v) 256}}

	# workaround for TCL 8.4 having no big-endian binary format
	# convert back to float and double
	foreach v {velocityx velocityy velocityz orientx orienty orientz} {
		set d($v) [cast_value $d($v) float]
	}
	foreach v {locationx locationy locationz} {
		set d($v) [cast_value $d($v) long]
	}
	foreach v [lsort [array names d]] {log [format "  %-20s %s" $v $d($v)]}
}

 2	{
	# FIRE PDU
	log "Fire PDU"
	if {[catch {binary scan $pdu ccccISSSSSSSSSSSSSSIWWWccSccccSSSSIIII \
		d(disver) d(exercise) d(pdukind) d(family) d(time) d(length) 0 \
		d(site) d(host) d(entity) d(sitetgt) d(hosttgt) d(enttgt) \
		d(sitemun) d(hostmun) d(entmun) d(siteevt) d(hostevt) d(entevt) \
		d(mission) d(locationx) d(locationy) d(locationz) \
		d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
		d(warhead) d(fuze) d(quantity) d(rate) \
		d(velocityx) d(velocityy) d(velocityz) d(range)} result]
	} {
		log $result
		return
	}
	set d(time) [decode_timestamp $d(time)]
	# workaround for TCL 8.4 having no big-endian binary format
	# convert back to float and double
	foreach v {velocityx velocityy velocityz} {
		set d($v) [cast_value $d($v) float]
	}
	foreach v {locationx locationy locationz} {
		set d($v) [cast_value $d($v) long]
	}
	foreach v [lsort [array names d]] {log [format "  %-20s %s" $v $d($v)]}
}

 3	{
	# DETONATION PDU
	log "Detonation PDU"
	if {[catch {binary scan $pdu ccccISSSSSSSSSSSSSSIIIWWWccSccccSSSSIIIccS \
		d(disver) d(exercise) d(pdukind) d(family) d(time) d(length) 0 \
		d(site) d(host) d(entity) d(sitetgt) d(hosttgt) d(enttgt) \
		d(sitemun) d(hostmun) d(entmun) d(siteevt) d(hostevt) d(entevt) \
		d(velocityx) d(velocityy) d(velocityz) \
		d(locationx) d(locationy) d(locationz) \
		d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
		d(warhead) d(fuze) d(quantity) d(rate) d(entx) d(enty) d(entz) d(result) \
		d(parts) d(art)} result]
	} {
		log $result
		return
	}
	set d(time) [decode_timestamp $d(time)]
	# workaround for TCL 8.4 having no big-endian binary format
	# convert back to float and double
	foreach v {velocityx velocityy velocityz} {
		set d($v) [cast_value $d($v) float]
	}
	foreach v {locationx locationy locationz} {
		set d($v) [cast_value $d($v) long]
	}
	foreach v [lsort [array names d]] {log [format "  %-20s %s" $v $d($v)]}
}

25	{
	# TRANSMIT PDU
	log "Transmit PDU"
	if {[catch {binary scan $pdu ccccISSSSSSccSccccccSWWWIIISSIIIISSSSSS \
		d(disver) d(exercise) d(pdukind) d(family) d(time) d(length) 0 \
		d(site) d(host) d(entity) d(radio) \
		d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
		d(state) d(source) 0 d(locationx) d(locationy) d(locationz) \
		d(entx) d(enty) d(entz) d(antenna) d(antlen) \
		d(freqhi) d(freqlo) d(bandwidth) d(power) d(spectrum) \
		d(modmajor) d(moddetail) d(system) d(crypto) d(cryptokey)} result]
	} {
		log $result
		return
	}
	set d(time) [decode_timestamp $d(time)]
	# workaround for TCL 8.4 having no big-endian binary format
	# convert back to float and double
	foreach v {entx enty entz bandwidth power} {
		set d($v) [cast_value $d($v) float]
	}
	foreach v {locationx locationy locationz} {
		set d($v) [cast_value $d($v) long]
	}
	foreach v [lsort [array names d]] {log [format "  %-20s %s" $v $d($v)]}
}

26	{
	# SIGNAL PDU
	log "Signal PDU"
	if {[catch {binary scan $pdu ccccISSSSSSSSISS \
		d(disver) d(exercise) d(pdukind) d(family) d(time) d(length) 0 \
		d(site) d(host) d(ent) d(radio) d(encoding) 0 d(rate) d(length) d(samples)} result]
	} {
		log $result
		return
	}
	set d(time) [decode_timestamp $d(time)]
	foreach v [lsort [array names d]] {log [format "  %-20s %s" $v $d($v)]}
}

default {
	# UNKNOWN PDU TYPE
#	log "heard PDU type $d(kind)"
	return
	}
} ;# end switch pdu kind
log ""
}


# create log widget
set f .f1
pack [frame $f] -anchor w -fill both -expand 1
scrollbar $f.x -orient horizontal -command "$f.txt xview"
scrollbar $f.y -command "$f.txt yview"
text $f.txt -background white -height 8 -width 50 -wrap none -undo 0 \
	-xscrollcommand "$f.x set" -yscrollcommand "$f.y set" -takefocus 0
grid $f.txt $f.y -sticky nsew
grid $f.x x -sticky nsew
grid rowconfigure $f 0 -weight 1
grid columnconfigure $f 0 -weight 1

set f .f2
pack [frame $f] -anchor w -fill x
label $f.porttxt -text {Port:}
entry $f.port -width 6 -bg white -textvariable port
button $f.open -text Connect -command {
	set x [open_socket $port]
	if {$x > 0} {set sock $x}
}
button $f.close -text Disconnect -command {close_socket $sock}
pack $f.porttxt $f.port $f.open $f.close -side left

set f .f3
pack [frame $f] -anchor w -fill x
checkbutton $f.autoscroll -text {Scroll to bottom} -variable autoscroll
button $f.clear -text Clear -command {.f1.txt delete 1.0 end}
button $f.console -text Console -command {catch {console show}}
pack $f.clear $f.autoscroll $f.console -anchor w -side left

.f2.open invoke
