# get_square_size --
#   gets the minimum square size for an input
# Arguments:
#   num		number
# Returns:
#   returns smallest square size that would fit number
#
proc get_square_size num {
    set i 1
    while {($i*$i) < $num} { incr i }
    return $i
}
