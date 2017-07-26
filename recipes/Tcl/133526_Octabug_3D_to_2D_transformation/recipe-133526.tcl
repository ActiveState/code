#!/bin/sh
# The next line is executed by /bin/sh, but not Tcl \
exec wish $0 ${1+"$@"}
##+##########################################################################
#
# Octabug
#
# Animates the morphing of a octahedron into an open cuboctahedron.
# by Keith Vetter
#
# Revisions:
# KPV Mar 07, 1995 - initial revision
# KPV Jun 07, 2002 - some minor code clean up
#
##+##########################################################################
#
# do_display
#
# Sets up the display
#
proc do_display {} {

    wm title . "Octabug"
    canvas .c -relief raised -borderwidth 4
    pack .c -side top
    .c config -height 600 -width 600

    xyz .eye "Eye Position" eye_ {5 4 3}

    frame .buttons
    button .anim -text Animate -command { set go [expr 1 - $go]; animate}
    button .qbtn -text Quit -command exit
    pack .buttons -side left -expand yes -fill both
    pack .anim .qbtn -side top -expand yes -in .buttons
}
##+##########################################################################
#
# animate
#
# Sets things in motion
#
proc animate {} {
    global go param

    if $go {
	set param [expr ($param + 1) % 100]
	triag
	after 1 animate
    }
}
##+##########################################################################
#
# Triag
#
# Draws all 8 triangles of the octabug.
#
proc triag {} {
    global mem param

    set t $param
    set t [expr $t*2.0/100]			;# Change to 0-2 range
    set t1 $t					;# Remember
    if {$t > 1} { set t [expr 2.0 - $t] }	;# Exploit symmetry
    set t [expr $t + 1.0]			;# 1.0-2.0 range

    .c delete poly
    if [info exists mem($t1,a)] {		;# Did we memoize entry already?
	set a $mem($t1,a)
	set b $mem($t1,b)
    } else {					;# Nope, recompute
	set d [expr sqrt(12 - 3 * $t * $t)]
	set a [expr (3*$t + $d) / 6]
	set b [expr $t - $a]
	if {$t1 > 1} {				;# In or out?
	    set d $a ; set a $b ; set b $d
	}

	set mem($t1,a) $a			;# Memoize--faster on next loop
	set mem($t1,b) $b
    }

    triag2 $a $b 7 -1 -1 -1			;# Draw all the triangles...
    triag2 $a $b 6 -1  1 -1			;# ...back to front if we can
    triag2 $a $b 5  1 -1 -1
    triag2 $a $b 4  1  1 -1
    triag2 $a $b 3 -1 -1  1
    triag2 $a $b 2 -1  1  1
    triag2 $a $b 1  1 -1  1
    triag2 $a $b 0  1  1  1

    update
}
##+##########################################################################
#
# Triag2
#
# Draws an individual triangle
#
proc triag2 {a b color x y z} {
    global colors
    set color [lindex $colors $color]

    set p1 [3d_obj2screen      0       [expr $y*$a] [expr $z*$b]]
    set p2 [3d_obj2screen [expr $x*$b]	    0	    [expr $z*$a]]
    set p3 [3d_obj2screen [expr $x*$a] [expr $y*$b]	 0	]
    eval .c create polygon $p1 $p2 $p3 -fill $color -tags poly
}
##+##########################################################################
#
# 3d Canvas
#
# Simple 3d canvas package. After specifying the eye, the page size and a
# few other variables, this package will draw points and lines in 3d space.
#
# This is very simple. No clipping, z-buffering, or rotation is provided.
#
# Procedures:
#  3d_init
#      Generates the transformation matrix needed to map from world to screen.
#      Must be called after setting or changing the eye, etc.
#  3d_obj2screen
#      Converts x,y,z of world coordinates into x,y of screen coordinates
#
# Variables:
#  3d(ex) 3d(ey) 3d(ez) == eye position
#  3d(rx) 3d(ry) 3d(rz) == reference point
#  3d(x)  3d(y)		== canvas size
#  3d(cx) 3d(cy)	== viewport center (reference point goes here)
#  3d(sx) 3d(sy)	== size of viewport
#

set 3d(ex)	5				;# Eye position
set 3d(ey)	4
set 3d(ez)	3
set 3d(rx)	0				;# Reference point
set 3d(ry)	0
set 3d(rz)	0
set 3d(x)	600				;# Page size
set 3d(y)	600
set 3d(cx)	[expr $3d(x) / 2.0]		;# Mid-point
set 3d(cy)	[expr $3d(y) / 2.0]
set 3d(sx)	[expr $3d(cx) - 5.0]		;# Viewport size
set 3d(sy)	[expr $3d(cy) - 6.0]

##+##########################################################################
#
# 3d_init
#
# Computes the transformation matrix for the current eye and center.
# Note, calling this resets all scaling, translations, etc.
#
proc 3d_init {} {
    global 3d_mat 3d

    if {$3d(ex) == 0 && $3d(ey) == 0} { set 3d(ey) .01 }

    set xy [expr sqrt($3d(ex)*$3d(ex) + $3d(ey)*$3d(ey))]
    set xyz [expr sqrt($xy*$xy + $3d(ez)*$3d(ez))]

    3d_ident 3d_mat
    3d_ident t					;# T0 - center to origin
    set t(3,0) [expr -$3d(rx)]
    set t(3,1) [expr -$3d(ry)]
    set t(3,2) [expr -$3d(rz)]
    3d_m44 3d_mat t 3d_mat
    3d_ident t					;# T1 -- Origin To Eye
    set t(3,0) [expr -$3d(ex)]
    set t(3,1) [expr -$3d(ey)]
    set t(3,2) [expr -$3d(ez)]
    3d_m44 3d_mat t 3d_mat
    3d_ident t					;# T2 -- Rotate 90 Around X
    set t(1,1)	0 ; set t(2,2) 0
    set t(1,2) -1 ; set t(2,1) 1
    3d_m44 3d_mat t 3d_mat
    3d_ident t					;# T3 -- rotate to eye line
    set t(0,0) [set t(2,2) [expr -$3d(ey) / $xy]]
    set t(0,2) [expr $3d(ex) / $xy]
    set t(2,0) [expr -$t(0,2)]
    3d_m44 3d_mat t 3d_mat
    3d_ident t					;# T4 -- Rotate To Eye Line
    set t(1,1) [set t(2,2) [expr $xy / $xyz]]
    set t(1,2) [expr $3d(ez) / $xyz]
    set t(2,1) [expr -$t(1,2)]
    3d_m44 3d_mat t 3d_mat
    3d_ident t					;# T5 -- Left-Handed Coords
    set t(2,2) -1
    3d_m44 3d_mat t 3d_mat
    3d_ident t					;# N - Scale By D/S
    set t(0,0) [set t(1,1) 4]
    3d_m44 3d_mat t 3d_mat
}
##+##########################################################################
#
# 3d_ident matrix
#
# Returns $mm as the identity matrix of size 4
#
proc 3d_ident mm {
    upvar 1 $mm m

    catch "uplevel [list unset $mm]"		;# Erase all entries
    foreach a {0,1 0,2 0,3 1,0 1,2 1,3 2,0 2,1 2,3 3,0 3,1 3,2} {
	set m($a) 0
    }
    set m(0,0) [set m(1,1) [set m(2,2) [set m(3,3) 1.0]]]
}
##+##########################################################################
#
# 3d_m44 ma mb mc
#
# Matrix multiply ma x mb => mc of size 4. mc can be either ma or mb.
#
proc 3d_m44 {ma mb mc} {
    upvar 1 $ma aa
    upvar 1 $mb bb
    upvar 1 $mc cc

    for {set r 0} {$r < 4} {incr r} {
	set result($r,0) [expr .0 + $aa($r,0)*$bb(0,0) + $aa($r,1)*$bb(1,0) \
		+ $aa($r,2)*$bb(2,0) + $aa($r,3)*$bb(3,0)]
	set result($r,1) [expr .0 + $aa($r,0)*$bb(0,1) + $aa($r,1)*$bb(1,1) \
		+ $aa($r,2)*$bb(2,1) + $aa($r,3)*$bb(3,1)]
	set result($r,2) [expr .0 + $aa($r,0)*$bb(0,2) + $aa($r,1)*$bb(1,2) \
		+ $aa($r,2)*$bb(2,2) + $aa($r,3)*$bb(3,2)]
	set result($r,3) [expr .0 + $aa($r,0)*$bb(0,3) + $aa($r,1)*$bb(1,3) \
		+ $aa($r,2)*$bb(2,3) + $aa($r,3)*$bb(3,3)]
    }

    catch "uplevel [list unset $mc]"
    foreach arr [array names result] {
	set cc($arr) $result($arr)
    }
}
##+##########################################################################
#
# 3d_obj2screen
#
# Converts a 3d position into 2d screen coordinates based on the current
# transformation matrix 3d_mat set up by 3d_init.
#
proc 3d_obj2screen {x y z} {
    global 3d_mat 3d

    set xe [expr $x*$3d_mat(0,0)+$y*$3d_mat(1,0)+$z*$3d_mat(2,0)+$3d_mat(3,0)]
    set ye [expr $x*$3d_mat(0,1)+$y*$3d_mat(1,1)+$z*$3d_mat(2,1)+$3d_mat(3,1)]
    set ze [expr $x*$3d_mat(0,1)+$y*$3d_mat(1,2)+$z*$3d_mat(2,2)+$3d_mat(3,2)]

    set sx [expr $3d(cx) + ($xe / $ze) * $3d(sx)]
    set sy [expr $3d(cx) - ($ye / $ze) * $3d(sy)]

    return [list $sx $sy]
}
##+##########################################################################
#
# 3d_axis
#
# Draws x,y,z axes
#
proc 3d_axis {c} {
    $c delete axis
    set o [3d_obj2screen 0 0 0]
    $c create line $o [3d_obj2screen 1.2 0 0] -fill black -arrow last -tag axis
    $c create line $o [3d_obj2screen 0 1.2 0] -fill black -arrow last -tag axis
    $c create line $o [3d_obj2screen 0 0 1.2] -fill black -arrow last -tag axis
}
##+##########################################################################
#
# Xyz
#
# Creates the subwindow with XYZ scales.
#
proc xyz {w title tag values} {
    global eyex eyey eyez centerx centery centerz num_steps

    catch {set x [expr round([lindex $values 0])]}
    catch {set y [expr round([lindex $values 1])]}
    catch {set z [expr round([lindex $values 2])]}
    set values [list $x $y $z]

    frame $w
    pack $w -side left -expand y;# -pady .1i

    label $w.ltitle -text $title -relief raised -bd 3
    bind $w.ltitle <Double-Button-1> reeye
    pack $w.ltitle -side top -fill x

    foreach l {x y z} {				;# Create 3 scales for x,y,z
	frame $w.f$l -bd 2 -relief raised	;# Holds scale & label
	scale $w.f$l.$l -from 10 -to 0 -relief ridge -length 75
	$w.f$l.$l config -var 3d(e$l) ;# -comm "redraw"
	bind $w.f$l.$l <ButtonRelease-1> "after 1 redraw"
	label $w.f$l.l$l -text [string toupper $l]
	$w.f$l.l$l config -bg [lindex [$w.f$l.$l config -bg] 4]
	pack $w.f$l -side left -expand yes
	pack $w.f$l.l$l $w.f$l.$l -side top -fill x

	$w.f$l.$l set [lindex $values 0]	;# Set the scale value
	set values [lrange $values 1 end]
    }

}
##+##########################################################################
#
# redraw
#
# Updates 3d stuff when eye position changes
#
proc redraw {} {
    global param

    3d_init
    triag
}
##+##########################################################################
#
# reeye
#
# Repositions the eye to the default location
#
proc reeye {} {
    global 3d
    set 3d(ex) 5 ; set 3d(ey) 4 ; set 3d(ez) 3
    redraw
}
##+##########################################################################
#############################################################################
#############################################################################
set go 0					;# Animation off
set param 0					;# Time parameter
set colors {red green blue cyan slateblue magenta chocolate yellow}

3d_init						;# Initialize the 3d world
do_display					;# Draw the display
triag						;# Draw initial shape
