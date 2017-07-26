variable symbols 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

proc add_baseX {numA numB} {
    # add two numbers in any base that can be expressed as a string of 
    # unique symbols
    #
    # John Ellson <ellson@lucent.com>

    variable symbols
    set base [string length $symbols]
    set idxA [string length $numA]
    set idxB [string length $numB]
    set carry 0
    set result ""
    while {$idxA || $idxB || $carry} {
	if {$idxA} {
	    set digA [string index $numA [incr idxA -1]]
	    set decA [string first $digA $symbols]
	    if {$decA < 0} {
		puts stderr "invalid digit \"$digA\""
		return -1
	    }
	} else {
	    set decA 0
	}
	if {$idxB} {
	    set digB [string index $numB [incr idxB -1]]
	    set decB [string first $digB $symbols]
	    if {$decB < 0} {
		puts stderr "invalid digit \"$digB\""
		return -1
	    }
	} else {
	    set decB 0
	}
	set sumdec [expr {$decA + $decB + $carry}]
	if {$sumdec >= $base} {
	    set carry 1
	    incr sumdec -$base
	} else {
	    set carry 0
	}
	set result [string index $symbols $sumdec]$result
    }
    return $result
}  
