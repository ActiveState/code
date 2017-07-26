namespace eval ::try {
   namespace export try
   variable bodyMatch {    \("uplevel" body line}; # Note: must be FOUR spaces
   variable usage {unknown keyword "%s" to try: should be "try body ?catch matcher body ...? ?finally body?"}

   # Some code that is factorised out.  It runs the given script in the context of our
   # caller's caller and, if that call generates an error, removes the extra junk inserted
   # into the error trace due to this.  All results are passed back by setting variables
   # in our caller's context...
   # The part argument gives the part of the error trace to insert into the error trace
   # in the case of an error occurring so as to indicate what the context of the error
   # w.r.t. the try command really is.
   proc helper {script part {eiv ei} {ecv ec} {codev code} {msgv msg}} {
      global errorInfo errorCode
      variable bodyMatch
      upvar 1 $eiv ei $ecv ec $codev code $msgv msg
      set code [catch [list uplevel 2 $script] msg]; # Note: unusual uplevel parameter
      set ec $errorCode
      set lines [split $errorInfo "\n"]
      if {$code == 1} {
         while {![regexp $bodyMatch [lindex $lines end]]} {
            set lines [lrange $lines 0 [expr {[llength $lines]-2}]]
         }
         regsub {"uplevel" body} [lindex $lines end] $part fixed
         set lines [lrange $lines 0 [expr {[llength $lines]-2}]]
         lappend lines $fixed
      }
      set ei [join $lines "\n"]
   }

   # The main command's implementation (see example for syntax.)
   proc try {body args} {

      # First, parse apart the args.  This is relatively straight-forward
      set hasFinally 0
      set catches {}
      for {set i 0} {$i<[llength $args]} {incr i} {
         set word [lindex $args $i]
         if {![string compare $word catch]} {
            if {$i+1 >= [llength $args]} {
               return -code error "missing matcher to catch"
            } elseif {$i+2 >= [llength $args]} {
               return -code error "missing body to catch"
            }
            lappend catches [lindex $args [incr i]]
            lappend catches [lindex $args [incr i]]
         } elseif {![string compare $word finally]} {
            if {$i+1 >= [llength $args]} {
               return -code error "missing body to finally"
            }
            set finally [lindex $args [incr i]]
            set hasFinally 1
         } else {
            variable usage
            return -code error [format $usage $word]
         }
      }

      # Now evaluate the body.  This updates variables "code", "ei", "ec" and "msg"
      # with the result code, the error trace, the error detail and the returned value
      # respectively...
      helper $body "try body"

      # Handle errors, if there were any.  Note that if an error does occur and gets
      # handled, the details of what the error was are lost as part of the processing.
      # Doing something more sophisticated is left as an exercise to the reader...
      if {$code == 1} {
         foreach {matcher handler} $catches {
            if {[string match $matcher $ec]} {
               helper $handler "catch \"$matcher\" body"
               break
            }
         }
      }

      # Do the finally clause.  This only wipes out the result information if the clause
      # causes an error.  Otherwise, the clause has no effect.  In particular, you cannot
      # (successfully) use return, break or continue in a finally clause.
      if {$hasFinally} {
         helper $finally "finally clause" a b c d
         if {$c} {
            set ei $a
            set ec $b
            set code $c
            set msg $d
         }
      }

      # Now we can return.  Phew!
      return -code $code -errorinfo $ei -errorcode $ec $msg
   }
}

namespace import ::try::try
