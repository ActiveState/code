proc scrollpane {w x y} {
   frame $w -class ScrollPane -width $x -height $y
   canvas $w.c -xscrollcommand [list $w.x set] -yscrollcommand [list $w.y set]
   scrollbar $w.x -orient horizontal -command [list $w.c xview]
   scrollbar $w.y -orient vertical   -command [list $w.c yview]
   set f [frame $w.c.content -borderwidth 0 -highlightthickness 0]
   $w.c create window 0 0 -anchor nw -window $f
   grid $w.c $w.y -sticky nsew
   grid $w.x      -sticky nsew
   grid rowconfigure    $w 0 -weight 1
   grid columnconfigure $w 0 -weight 1
   # This binding makes the scroll-region of the canvas behave correctly as
   # you place more things in the content frame.
   bind $f <Configure> [list scrollpane_cfg $w %w %h]
   $w.c configure -borderwidth 0 -highlightthickness 0
   return $f
}
proc scrollpane_cfg {w wide high} {
   set newSR [list 0 0 $wide $high]
   if {![string equals [$w cget -scrollregion] $newSR]} {
      $w configure -scrollregion $newSR
   }
}

### Demo code ###
set sp [scrollpane .s 95 235]
pack .s -fill both
pack [button .quit -text Quit -command exit] -fill both
for {set i 0} {$i<25} {incr i} {
   set text "This is button #$i of a sequence"
   pack [button $sp.b$i -text $text -command [list puts HI-$i]]
}
