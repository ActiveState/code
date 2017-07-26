proc o args {
    # combine the functions in args, return the created name
    set name [info level 0]
    set body "[join $args " \["] \$x"
    append body [string repeat \] [expr {[llength $args]-1}]]
    proc $name x $body
    set name
}
# Now for the rendering framework:
proc fim {f {zoom 100} {width 200} {height -}} {
    # produce a photo image by applying function f to pixels
    if {$height=="-"} {set height $width}
    set im [image create photo -height $height -width $width]
    set data {}
    set xs {}
    for {set j 0} {$j<$width} {incr j} {
        lappend xs [expr {($j-$width/2.)/$zoom}]
    }
    for {set i 0} {$i<$height} {incr i} {
        set row {}
        set y [expr {($i-$height/2.)/$zoom}]
        foreach x $xs {
            lappend row [$f [list $x $y]]
        }
        lappend data $row
    }
    $im put $data
    set im
}
if 0 {Basic imaging functions ("drawers") have the common
functionality ''point -> color'', where point is a pair {x y} (or,
after applying a polar transform, {r a}...) and ''color'' is a Tk color
name, like "green" or #010203:}
proc  vstrip p {
    # a simple vertical bar
    b2c [expr {abs([lindex $p 0]) < 0.5}]
}
proc udisk p {
    # unit circle with radius 1
    foreach {x y} $p break
    b2c [expr {hypot($x,$y) < 1}]
}
proc xor {f1 f2 p} {
    lappend f1 $p; lappend f2 $p
    b2c [expr {[eval $f1] != [eval $f2]}]
}
proc and {f1 f2 p} {
    lappend f1 $p; lappend f2 $p
    b2c [expr {[eval $f1] == "#000" && [eval $f2] == "#000"}]
}
proc checker p {
    # black and white checkerboard
    foreach {x y} $p break
    b2c [expr {int(floor($x)+floor($y)) % 2 == 0}]
}
proc gChecker p {
    # greylevels correspond to fractional part of x,y
    foreach {x y} $p break
    g2c [expr {(fmod(abs($x),1.)*fmod(abs($y),1.))}]
}
proc bRings p {
    # binary concentric rings
    foreach {x y} $p break
    b2c [expr {round(hypot($x,$y)) % 2 == 0}]
}
proc gRings p {
    # grayscale concentric rings
    foreach {x y} $p break
    g2c [expr {(1 + cos(3.14159265359 * hypot($x,$y))) / 2.}]
}
proc radReg {n p} {
    # n wedge slices starting at (0,0)
    foreach {r a} [toPolars $p] break
    b2c [expr {int(floor($a*$n/3.14159265359))%2 == 0}]
}
proc xPos p {b2c [expr {[lindex $p 0]>0}]}
proc cGrad p {
    # color gradients - best watched at zoom=100
    foreach {x y} $p break
    if {abs($x)>1.} {set x 1.}
    if {abs($y)>1.} {set y 1.}
    set r [expr {int((1.-abs($x))*255.)}]
    set g [expr {int((sqrt(2.)-hypot($x,$y))*180.)}]
    set b [expr {int((1.-abs($y))*255.)}]
    c2c $r $g $b
}
if 0 {Beyond the examples in Conal Elliott's paper, I found out that 
function imaging can also be abused for a (slow and imprecise) function plotter, 
which displays the graph for <I>y = f(x)</I> if you call it with <I>$y + 
f($x)</I> as first argument:}

proc fplot {expr p} {
    foreach {x y} $p break
    b2c [expr abs($expr)<=0.04] ;# double eval required here!
}

if 0 {Here is a combinator for two binary images that shows in different 
colors for which point both or either are "true" - nice but slow:}
proc bin2 {f1 f2 p} {
    set a [eval $f1 [list $p]]
    set b [eval $f2 [list $p]]
    expr {
        $a == "#000" ?
	$b == "#000" ? "green"
	: "yellow"
        : $b == "#000" ? "blue"
        : "black"
    }
}
#--------------------------------------- Pixel converters:
proc g2c {greylevel} {
    # convert 0..1 to #000000..#FFFFFF
    set hex [format %02X [expr {round($greylevel*255)}]]
    return #$hex$hex$hex
}
proc b2c {binpixel} {
    # 0 -> white, 1 -> black
    expr {$binpixel? "#000" : "#FFF"}
}
proc c2c {r g b} {
    # make Tk color name: {0 128 255} -> #0080FF
    format #%02X%02X%02X $r $g $b
}
proc bPaint {color0 color1 pixel} {
    # convert a binary pixel to one of two specified colors
    expr {$pixel=="#000"? $color0 : $color1}
}

if 0 {This painter colors a grayscale image in hues of the given color. It 
normalizes the given color through dividing by the corresponding values for 
"white", but appears pretty slow too:}

proc gPaint {color pixel} {
    set abspixel [lindex [rgb $pixel] 0]
    set rgb [rgb $color]
    set rgbw [rgb white]
    foreach var {r g b} in $rgb ref $rgbw {
        set $var [expr {round(double($abspixel)*$in/$ref/$ref*255.)}]
    }
    c2c $r $g $b
}

if 0 {This proc caches the results of [winfo rgb] calls, because these are 
quite expensive, especially on remote X displays - <A 
href="http://mini.net/tcl/2683">rmax</A>}

proc rgb {color} {
    upvar "#0" rgb($color) rgb
    if {![info exists rgb]} {set rgb [winfo rgb . $color]}
    set rgb
}
#------------------------------ point -> point transformers
proc fromPolars p {
    foreach {r a} $p break
    list [expr {$r*cos($a)}] [expr {$r*sin($a)}]
}
proc toPolars p {
    foreach {x y} $p break
    list [expr {hypot($x,$y)}] [expr {atan2($y,$x)}]
}
proc radInvert p {
    foreach {r a} [toPolars $p] break
    fromPolars [list [expr {$r? 1/$r: 9999999}] $a]
}
proc rippleRad {n s p} {
    foreach {r a} [toPolars $p] break
    fromPolars [list [expr {$r*(1.+$s*sin($n*$a))}] $a]
}
proc slice {n p} {
    foreach {r a} $p break
    list $r [expr {$a*$n/3.14159265359}]
}
proc rotate {angle p} {
    foreach {x y} $p break
    set x1 [expr {$x*cos(-$angle) - $y*sin(-$angle)}]
    set y1 [expr {$y*cos(-$angle) + $x*sin(-$angle)}]
    list $x1 $y1
}
proc swirl {radius p} {
    foreach {x y} $p break
    set angle [expr {hypot($x,$y)*6.283185306/$radius}]
    rotate $angle $p
}

if 0 {Now comes the demo program. It shows the predefined basic image 
operators, and some combinations, on a button bar. Click on one, have some 
patience, and the corresponding image will be displayed on the canvas to the 
right. You can also experiment with image operators in the entry widget at 
bottom - hit <Return> to try. The text of sample buttons is also copied to 
the entry widget, so you can play with the parameters, or rewrite it as you 
wish. Note that a well-formed <I>funimj</I> composition consists of: 
<UL>
<LI>the composition operator "o" 
<LI>zero or more "painters" (color -> color) 
<LI>one "drawer" (point -> color) 
<LI>zero or more "transformers" (point -> point) </LI></UL>}

proc fim'show {c f} {
    $c delete all
    set ::try $f ;# prepare for editing
    set t0 [clock seconds]
    . config -cursor watch
    update ;# to make the cursor visible
    $c create image 0 0 -anchor nw -image [fim $f $::zoom]
    wm title . "$f: [expr [clock seconds]-$t0] seconds"
    . config -cursor {}
}
proc fim'try {c varName} {
    upvar #0 $varName var
    $c delete all
    if [catch {fim'show $c [eval $var]}] {
        $c create text 10 10 -anchor nw -text $::errorInfo
    }
}
# Composed functions need only be mentioned once,
# which creates them, and they can later be picked up
# by [info procs]. The o looks nicely bullet-ish here..
o bRings
o cGrad
o checker
o gRings
o vstrip
o xPos
o {bPaint brown beige} checker
o checker {slice 10} toPolars
o checker {rotate 0.1}
o vstrip {swirl 1.5}
o checker {swirl 16}
o {fplot {$y + exp($x)}}
o checker radInvert
o gRings {rippleRad 8 0.3}
o xPos {swirl .75}
o gChecker
o {gPaint red} gRings
o {bin2 {radReg 7} udisk}

#----------------------------------------------- testing
frame .f2
set c [canvas .f2.c]
set e [entry .f2.e -bg white -textvar try]
bind $e <Return> [list fim'try $c ::try]
scale .f2.s -from 1 -to 100 -variable zoom -ori hori -width 6
#--------------------------------- button bar:
frame .f
set n 0
foreach imf [lsort [info procs "o *"]] {
    button .f.b[incr n] -text $imf -anchor w -pady 0 \
	    -command [list fim'show $c $imf]
}
set ::zoom 25
eval pack [winfo children .f] -side top -fill x -ipady 0
eval pack [winfo children .f2] -side top -fill x
pack .f .f2 -side left -anchor n
bind . <Escape> {exec wish $argv0 &; exit} ;# dev helper
bind . ? {console show} ;# dev helper, Win/Mac only
