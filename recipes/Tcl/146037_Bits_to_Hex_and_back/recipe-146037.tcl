# bin2hex --
#   converts binary to hex number
# Arguments:
#   bin		number in binary format
# Returns:
#   hexadecimal number
#
proc bin2hex bin {
    ## No sanity checking is done
    array set t {
	0000 0 0001 1 0010 2 0011 3 0100 4
	0101 5 0110 6 0111 7 1000 8 1001 9
	1010 a 1011 b 1100 c 1101 d 1110 e 1111 f
    }
    set diff [expr {4-[string length $bin]%4}]
    if {$diff != 4} {
        set bin [format %0${diff}d$bin 0]
    }
    regsub -all .... $bin {$t(&)} hex
    return [subst $hex]
}


# hex2bin --
#   converts hex number to bin
# Arguments:
#   hex		number in hex format
# Returns:
#   binary number (in chars, not binary format)
#
proc hex2bin hex {
    set t [list 0 0000 1 0001 2 0010 3 0011 4 0100 \
	    5 0101 6 0110 7 0111 8 1000 9 1001 \
	    a 1010 b 1011 c 1100 d 1101 e 1110 f 1111 \
	    A 1010 B 1011 C 1100 D 1101 E 1110 F 1111]
    regsub {^0[xX]} $hex {} hex
    return [string map -nocase $t $hex]
}

# hex2bin-alternate --
#   converts hex number to bin
# Arguments:
#   hex		number in hex format
# Returns:
#   binary number (in chars, not binary format)
#

proc bin2hex-alternate bin {
    ## No sanity checking is done
    set t {
	0000 0 0001 1 0010 2 0011 3 0100 4
	0101 5 0110 6 0111 7 1000 8 1001 9
	1010 a 1011 b 1100 c 1101 d 1110 e 1111 f
    }
    set diff [expr {4-[string length $bin]%4}]
    if {$diff != 4} {
        set bin [format %0${diff}d$bin 0]
    }
    return [string map $t $hex]
}
