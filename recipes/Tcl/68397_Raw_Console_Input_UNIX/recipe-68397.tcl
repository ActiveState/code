# Helper procedure
proc stty args {
   eval [list exec /bin/stty <@/dev/tty] $args
}

proc yesOrNo {prompt} {
   # Save the current state; makes it easier to reset!
   set savedStty [stty -g]

   # Turn off echoing and turn on raw input
   stty -echo raw

   # Prompt!
   puts -nonewline "$prompt [Y/N] "
   flush stdout

   set answer ?

   # Get input as yes or no, or sound the terminal bell...
   while {1} {
      switch [string tolower [read stdin 1]] {
         y {set answer yes; puts YES; break}
         n {set answer no;  puts NO;  break}
         default {puts -nonewline \a; flush stdout}
      }
   }

   # Put things back as they were; this is IMPORTANT!
   stty $savedStty

   return $answer
}

# DEMO CODE!
if {[yesOrNo "Frobnicate the manglewurzel?"]} {
   frobnicate manglewurzel
}
