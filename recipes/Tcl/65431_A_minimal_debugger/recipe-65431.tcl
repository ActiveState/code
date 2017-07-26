proc bp {{s {}}} {
    if {![info exists ::bp_skip]} {
	set ::bp_skip [list]
    } elseif {[lsearch -exact $::bp_skip $s]>=0} {
	return
    }
    set who [info level -1]
    while 1 {
	# Display prompt and read command.
	puts -nonewline "$who/$s> "; flush stdout
	gets stdin line

	# Handle shorthands
	if {$line=="c"} {puts "continuing.."; break}
	if {$line=="i"} {set line "info locals"}

	# Handle everything else.
	catch {uplevel 1 $line} res
	puts $res
    }
}
