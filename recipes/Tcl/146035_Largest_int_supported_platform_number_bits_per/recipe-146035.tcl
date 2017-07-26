# largest_int --
#   Finds the largest recognized int in Tcl for the platform
# Arguments:
#   none
# Results:
#   Returns the largest allowed value for an int (for exprs and stuff)
#
proc largest_int {} {
    set int 1
    set exp 7; # assume we get at least 8 bits
    while {$int > 0} { set int [expr {1 << [incr exp]}] }
    expr {$int-1}
}

# int_bits --
#   Finds the number of bits in an int
# Arguments:
#   none
# Results:
#   Returns the numbers of bits in an int
#
proc int_bits {} {
    set int 1
    set exp 7; # assume we get at least 8 bits
    while {$int > 0} { set int [expr {1 << [incr exp]}] }
    # pop up one more, since we start at 0
    incr exp
}
