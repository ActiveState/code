# random --
#
#	Return a number in the range 0 .. $range-1
#
# Arguments:
#	range    integer range constraint
#
# Results:
#	Number in range [0..$range)
#
proc random {{range 100}} {
    return [expr {int(rand()*$range)}]
}
