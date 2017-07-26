proc base_characters {base_n} {
    set base [list 0 1 2 3 4 5 6 7 8 9 A B C D E F G H I J K L M \
	    N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p \
	    q r s t u v w x y z]
    if {$base_n < 2 || $base_n > 62} {
	error "Invalid base \"$base_n\" (should be an integer between 2 and 62)"
    }
    return [lrange $base 0 [expr $base_n - 1]]
}

proc base_n_to_decimal {number base_n} {
    set base   [base_characters $base_n]
    # trim white space in case [format] is used
    set number [string trim $number]
    # bases 11 through 36 can be treated in a case-insensitive fashion
    if {$base_n <= 36} {
	set number [string toupper $number]
    }
    set decimal 0
    set power [string length $number]

    foreach char [split $number ""] {
	incr power -1
	set dec_val [lsearch $base $char]
	if {$dec_val == -1} {
	    error "$number is not a valid base $base_n number"
	}
	set decimal [expr $decimal + $dec_val * int(pow($base_n,$power))]
    }

    return $decimal
}

proc decimal_to_base_n {number base_n} {
    set base [base_characters $base_n]
    # trim white space in case [format] is used
    set number [string trim $number]

    if {![string is integer $number] || $number < 0} {
	error "$number is not a base-10 integer between 0 and 2147483647"
    }

    while 1 {
	set quotient  [expr $number / $base_n]
	set remainder [expr $number % $base_n]
	lappend remainders $remainder
	set number $quotient
	if {$quotient == 0} {
	    break
	}
    }

    set base_n [list]

    for {set i [expr [llength $remainders] - 1]} {$i >= 0} {incr i -1} {
	lappend base_n [lindex $base [lindex $remainders $i]]
    }

    return [join $base_n ""]

}

proc convert_number {number "from" "base" base_from "to" "base" base_to} {
    return [decimal_to_base_n [base_n_to_decimal $number $base_from] $base_to]
}
