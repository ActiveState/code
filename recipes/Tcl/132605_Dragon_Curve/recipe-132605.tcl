 ####################################################################
 #
 # dragon.tcl
 #
 # Draws a dragon curve
 # by Keith Vetter
 #
 # Revisions:
 # KPV May 09, 2002 - initial revision
 #
 # http://www.math.okstate.edu/mathdept/dynamics/lecnotes/node17.html
 ####################################################################

 set cw 500 ; set ch 500  ;# canvas size
 array set comp {R L L R}
 array set turn {E,R S E,L N S,R W S,L E W,R N W,L S N,R E N,L W}
 array set fill {E cyan S magenta W blue N yellow}

 proc DoDisplay {} {
     global cw cw2 ch ch2
     canvas .c -width $cw -height $ch -bd 2 -relief ridge
     set cw2 [expr {$cw / 2}]
     set ch2 [expr {$ch / 2}]
     .c config -scrollregion [list -$cw2 -$ch2 $cw2 $ch2]
     .c yview moveto .5
     .c xview moveto .5
     .c create oval -5 -5 5 5 -fill yellow -tag o
     .c create text -$cw2 -$ch2 -anchor nw -font bold -tag lbl
     pack .c -side top

     scale .deg -label Degree -orient horizontal -from 1 -to 12
     .deg config -relief ridge -showvalue 1
     .deg set 4
     bind .deg  <ButtonRelease-1> [list after 1 [list DrawDragons -1]]

     pack .deg -side left
 }

 # DrawDragons -- draw four dragon curve of this degree
 proc DrawDragons {n} {
     .c config -cursor watch
     if {$n == -1} {set n [.deg get]} else {.deg set $n}
     .c delete dragon
     .c itemconfig lbl -text "Dragon Curve: $n"
     DrawDragon $n E ; update
     DrawDragon $n W ; update
     DrawDragon $n S ; update
     DrawDragon $n N ; update
     .c config -cursor {}

 }
 # DrawDragon -- draw one dragon curve of this degree and orientation
 proc DrawDragon {n {dir E}} {
     global cw2 ch2 fill
     set dir [string toupper $dir]

     set tag "dragon_$dir"
     set coords [GetCoords $n $dir]
     set coords [ScaleCoords $coords]
     .c create line $coords -tag [list dragon $tag] -width 2 -fill $fill($dir)

     .c raise o
     .c raise lbl
 }
 # ScaleCoords -- scale the unit coords to fit into the window
 proc ScaleCoords {coords} {
     global cw2 ch2                              ;# Window size

     # Find max coordinate from origin
     set max_x [set max_y [set min_x [set min_y 0]]]
     foreach {x y} $coords {
         if {$x > $max_x} {set max_x $x
         } elseif {$x < $min_x} {set min_x $x}
         if {$y > $max_y} {set max_y $y
         } elseif {$y < $min_y} {set min_y $y}
     }
     set max_x [expr {-$min_x > $max_x ? -$min_x : $max_x}]
     set max_y [expr {-$min_y > $max_y ? -$min_y : $max_y}]
     set max [expr {$max_x > $max_y ? $max_x : $max_y}]

     set sc [expr {($cw2 - 50) / $max}]

     set new {}
     foreach {x y} $coords {
         set nx [expr {$x * $sc}] ; set ny [expr {$y * $sc}]
         lappend new $nx $ny
     }
     return $new
 }
 # GetCoords -- get the unit coordinates for this degree curve
 proc GetCoords {n dir} {
     global turn

     set turns $dir
     foreach leg [MakeDragon $n] {
         set dir $turn($dir,$leg)
         lappend turns $dir
     }

     set x 0 ; set y 0
     set coords [list $x $y]
     foreach leg $turns {
         if {$leg == "E"}       { incr x
         } elseif {$leg == "S"} { incr y
         } elseif {$leg == "W"} { incr x -1
         } elseif {$leg == "N"} { incr y -1 }
         lappend coords $x $y
     }

     return $coords
 }
 # MakeDragon -- gets the turn data for this degree dragon curve
 proc MakeDragon {n} {
     global dragon

     # Do we already have it?
     if {[info exists dragon($n)]} { return $dragon($n) }
     if {$n == 0} { return {}}

     # dragon(n) = dragon(n-1) + "R" + reverse(complement(dragon(n-1)))
     set last [MakeDragon [expr {$n - 1}]]
     set dragon($n) $last
     lappend dragon($n) R

     set idx [llength $last]
     while {[incr idx -1] >= 0} {
         set item [lindex $last $idx]
         lappend dragon($n) $::comp($item)
     }

     return $dragon($n)
 }

 DoDisplay
 DrawDragons 4
