package require Tk
proc gradImage {{w6 100}} {
    set im [image create photo -width $w6 -height 256]
    set w1 [expr {$w6 / 6}]
    set w2 [expr {$w1 * 2}]; set w3 [expr {$w1 * 3}]
    set w4 [expr {$w1 * 4}]; set w5 [expr {$w1 * 5}]
    for {set i 0; set j 1} {$i < 256} {incr i; incr j} {
	set x [format %2.2x $i]
	$im put "#${x}0000" -to 0   $i $w1 $j
	$im put "#00${x}00" -to $w1 $i $w2 $j
	$im put "#0000${x}" -to $w2 $i $w3 $j
	$im put "#${x}FFFF" -to $w3 $i $w4 $j
	$im put "#FF${x}FF" -to $w4 $i $w5 $j
	$im put "#FFFF${x}" -to $w5 $i $w6 $j
    }
    return $im
}

set im [gradImage 300]
pack [canvas .c -bd 0 -highlightthickness 0 -height 256 -width 300]
.c create image 0 0 -anchor nw -image $im -tag im
# Click in the image to get the {R G B} tuple
.c bind im <Button-1> { puts [$im get %x %y] }
