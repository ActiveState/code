# The shapes of individual elements of a digit.  They were worked out
# with a piece of paper, a calculator and a good deal of head-scratching.
array set lcdshape {
   a {3.0 5 5.2 3 7.0 5 6.0 15 3.8 17 2.0 15}
   b {6.3 2 8.5 0 18.5 0 20.3 2 18.1 4 8.1 4}
   c {19.0 5 21.2 3 23.0 5 22.0 15 19.8 17 18.0 15}
   d {17.4 21 19.6 19 21.4 21 20.4 31 18.2 33 16.4 31}
   e {3.1 34 5.3 32 15.3 32 17.1 34 14.9 36 4.9 36}
   f {1.4 21 3.6 19 5.4 21 4.4 31 2.2 33 0.4 31}
   g {4.7 18 6.9 16 16.9 16 18.7 18 16.5 20 6.5 20}
}
# Which elements are turned on for a given digit?  Note that this is only
# decimal digits, though adding hex digits should be easy enough.
array set llcd {
   0 {a b c d e f}
   1 {c d}
   2 {b c e f g}
   3 {b c d e g}
   4 {a c d g}
   5 {a b d e g}
   6 {a b d e f g}
   7 {b c d}
   8 {a b c d e f g}
   9 {a b c d e g}
   - {g}
   { } {}
}
# Which elements are turned off for a given digit?  Note that you should make
# sure that this is the complement of the digits set in the llcd array...
array set ulcd {
   0 {g}
   1 {a b e f g}
   2 {a d}
   3 {a f}
   4 {b e f}
   5 {c f}
   6 {c}
   7 {a e f g}
   8 {}
   9 {f}
   - {a b c d e f}
   { } {a b c d e f g}
}

# Displays a decimal number using LCD digits in the top-left of the canvas
proc showLCD {
   canvas number {width 5} {colours {#ff8080 #ff0000 #404040 #303030}}
} {
   global llcd ulcd lcdshape
   set lcdoffset 0

   # Remove previous LCD number
   $canvas delete lcd

   # Get colours to draw with
   foreach {onRim onFill offRim offFill} $colours {break}

   # For each digit in the (space-padded) number...
   foreach glyph [split [format %${width}d $number] {}] {
      # ... draw its "on" elements...
      foreach symbol $llcd($glyph) {
         # ... by drawing a polygon and shifting it...
         $canvas move [eval $canvas create polygon $lcdshape($symbol)                  -tags lcd -outline $onRim -fill $onFill] $lcdoffset 0
      }
      # ... and then doing the same thing for the "off" elements
      foreach symbol $ulcd($glyph) {
         $canvas move [eval $canvas create polygon $lcdshape($symbol)                  -tags lcd -outline $offRim -fill $offFill] $lcdoffset 0
      }
      # And now we increase our offset too...
      incr lcdoffset 22
   }
}
