package require Tcl 8.3

 #----------------------------------------------------------------------
 #
 # dumpFile --
 #
 #       Produce a hex/ASCII dump of a file.
 #
 # Parameters:
 #       fileName -- Path name of the file
 #       channel  -- (Optional) Channel on which to produce the dump.
 #                   Default is stdout.
 #
 # Results:
 #       None.
 #
 # Side effects:
 #       The file is opened, dumped to the specified channel, and
 #       closed again.
 #
 #----------------------------------------------------------------------

 proc dumpFile { fileName { channel stdout } } {

     # Open the file, and set up to process it in binary mode.

     set f [open $fileName r]
     fconfigure $f \
         -translation binary \
         -encoding binary \
         -buffering full -buffersize 16384

     while { 1 } {

         # Record the seek address.  Read 16 bytes from the file.

         set addr [tell $f]
         set s [read $f 16]

         # Convert the data to hex and to characters.

         binary scan $s H*@0a* hex ascii

         # Replace non-printing characters in the data.

         regsub -all {[^[:graph:] ]} $ascii {.} ascii

         # Split the 16 bytes into two 8-byte chunks

         set hex1 [string range $hex 0 15]
         set hex2 [string range $hex 16 31]
         set ascii1 [string range $ascii 0 7]
         set ascii2 [string range $ascii 8 16]

         # Convert the hex to pairs of hex digits

         regsub -all {..} $hex1 {& } hex1
         regsub -all {..} $hex2 {& } hex2

         # Put the hex and Latin-1 data to the channel

         puts $channel [format {%08x  %-24s %-24s %-8s %-8s} \
                            $addr $hex1 $hex2 $ascii1 $ascii2]

         # Stop if we've reached end of file

         if { [string length $s] == 0 } {
             break
         }
     }

     # When we're done, close the file.

     close $f
     return
 }

 #----------------------------------------------------------------------
 #
 # Main program
 #
 #----------------------------------------------------------------------

 if { [info exists argv0] && [string equal $argv0 [info script]] } {
     foreach file $argv {
	 puts "$file:"
	 dumpFile $file
     }
 }
