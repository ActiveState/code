# rgb2dec --
#
#   Turns #rgb into 3 elem list of decimal vals.
#
# Arguments:
#   c		The #rgb hex of the color to translate
# Results:
#   Returns a #RRGGBB or #RRRRGGGGBBBB color
#
proc rgb2dec c {
    set c [string tolower $c]
    if {[regexp -nocase {^#([0-9a-f])([0-9a-f])([0-9a-f])$} $c x r g b]} {
	# double'ing the value make #9fc == #99ffcc
	scan "$r$r $g$g $b$b" "%x %x %x" r g b
    } else {
	if {![regexp {^#([0-9a-f]+)$} $c junk hex] || \
		[set len [string length $hex]]>12 || $len%3 != 0} {
	    if {[catch {winfo rgb . $c} rgb]} {
		return -code error "bad color value \"$c\""
	    } else {
		return $rgb
	    }
	}
	set len [expr {$len/3}]
    	scan $hex "%${len}x%${len}x%${len}x" r g b
    }
    return [list $r $g $b]
}

# dec2rgb --
#
#   Takes a color name or dec triplet and returns a #RRGGBB color.
#   If any of the incoming values are greater than 255,
#   then 16 bit value are assumed, and #RRRRGGGGBBBB is
#   returned, unless $clip is set.
#
# Arguments:
#   r		red dec value, or list of {r g b} dec value or color name
#   g		green dec value, or the clip value, if $r is a list
#   b		blue dec value
#   clip	Whether to force clipping to 2 char hex
# Results:
#   Returns a #RRGGBB or #RRRRGGGGBBBB color
#
proc dec2rgb {r {g 0} {b UNSET} {clip 0}} {
    if {![string compare $b "UNSET"]} {
	set clip $g
	if {[regexp {^-?(0-9)+$} $r]} {
	    foreach {r g b} $r {break}
	} else {
	    foreach {r g b} [winfo rgb . $r] {break}
	}
    } 
    set max 255
    set len 2
    if {($r > 255) || ($g > 255) || ($b > 255)} {
	if {$clip} {
	    set r [expr {$r>>8}]; set g [expr {$g>>8}]; set b [expr {$b>>8}]
	} else {
	    set max 65535
	    set len 4
	}
    }
    return [format "#%.${len}X%.${len}X%.${len}X" \
	    [expr {($r>$max)?$max:(($r<0)?0:$r)}] \
	    [expr {($g>$max)?$max:(($g<0)?0:$g)}] \
	    [expr {($b>$max)?$max:(($b<0)?0:$b)}]]
}

# shade --
#
#   Returns a shade between two colors
#
# Arguments:
#   orig	start #rgb color
#   dest	#rgb color to shade towards
#   frac	fraction (0.0-1.0) to move $orig towards $dest
# Results:
#   Returns a shade between two colors based on the
# 
proc shade {orig dest frac} {
    if {$frac >= 1.0} { return $dest } elseif {$frac <= 0.0} { return $orig }
    foreach {origR origG origB} [rgb2dec $orig] \
	    {destR destG destB} [rgb2dec $dest] {
	set shade [format "\#%02x%02x%02x" \
		[expr {int($origR+double($destR-$origR)*$frac)}] \
		[expr {int($origG+double($destG-$origG)*$frac)}] \
		[expr {int($origB+double($destB-$origB)*$frac)}]]
	return $shade
    }
}

# complement --
#
#   Returns a complementary color
#   Does some magic to avoid bad complements of grays
#
# Arguments:
#   orig	start #rgb color
# Results:
#   Returns a complement of a color
# 
proc complement {orig {grays 1}} {
    foreach {r g b} [rgb2dec $orig] {break}
    set R [expr {(~$r)%256}]
    set G [expr {(~$g)%256}]
    set B [expr {(~$b)%256}]
    if {$grays && abs($R-$r) < 32 && abs($G-$g) < 32 && abs($B-$b) < 32} {
	set R [expr {($r+128)%256}]
	set G [expr {($g+128)%256}]
	set B [expr {($b+128)%256}]
    }
    return [format "\#%02x%02x%02x" $R $G $B]
}
