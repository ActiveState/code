# hsv2rgb --
#
#   Convert hsv to rgb
#
# Arguments:
#   h		hue
#   s		saturation
#   v		value
# Results:
#   Returns an rgb triple from hsv
# 
proc hsv2rgb {h s v} {
    if {$s <= 0.0} {
	# achromatic
	set v [expr {int($v)}]
	return "$v $v $v"
    } else {
	set v [expr {double($v)}]
        if {$h >= 1.0} { set h 0.0 }
        set h [expr {6.0 * $h}]
        set f [expr {double($h) - int($h)}]
        set p [expr {int(256 * $v * (1.0 - $s))}]
        set q [expr {int(256 * $v * (1.0 - ($s * $f)))}]
        set t [expr {int(256 * $v * (1.0 - ($s * (1.0 - $f))))}]
	set v [expr {int(256 * $v)}]
        switch [expr {int($h)}] {
            0 { return "$v $t $p" }
            1 { return "$q $v $p" }
	    2 { return "$p $v $t" }
	    3 { return "$p $q $v" }
	    4 { return "$t $p $v" }
	    5 { return "$v $p $q" }
        }
    }
}
