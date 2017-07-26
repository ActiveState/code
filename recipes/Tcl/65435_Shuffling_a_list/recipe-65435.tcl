proc K { x y } { set x }

proc shuffle4 { list } {
    set n [llength $list]
    while {$n > 0} {
	set j [expr {int(rand()*$n)}]
	lappend slist [lindex $list $j]
	incr n -1
	set temp [lindex $list $n]
	set list [lreplace [K $list [set list {}]] $j $j $temp]
    }
    return $slist
}
