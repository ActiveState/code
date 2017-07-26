proc dec2hex {value} {
   # Creates a 32 bit hex number from a signed decimal number
   # Replace all non-decimal characters
   regsub -all {[^0-9\.\-]} $value {} newtemp
   set value [string trim $newtemp]
   if {$value < 2147483647 && $value > -2147483648} {
      set tempvalue [format "%#010X" [expr $value]]
      return [string range $tempvalue 2 9]
   } elseif {$value < -2147483647} {
      return "80000000"
   } else {
      return "7FFFFFFF"
   }
}

proc dec2hex16 {value} {
   # Creates a 16 bit hex number from a signed decimal number
   # Replace all non-decimal characters
   regsub -all {[^0-9\.\-]} $value {} newtemp
   set value [string trim $newtemp]
   if {$value < 32767 && $value > -32768} {
      set tempvalue [format "%#010X" [expr $value]]
      return [string range $tempvalue 6 9]
   } elseif {$value < -32767} {
      return "8000"
   } else {
      return "7FFF"
   }
}

proc hex2dec {hexvalue} {
   # Creates an unsigned decimal number from a 63 bit hex value
    set total "0000000000000000"
   set mask "7FFFFFFF"
   # replace from the end
    set start 15
   # Replace all non-hex characters
   regsub -all {[^0-9A-F\.\-]} $hexvalue {} newtemp
   set hexvalue [string trim $newtemp]
   # Go from the end to the start
    for {set i [expr [string length $hexvalue] -1]} {$i > -1} {incr i -1} {
      # Get the next hex digit
        set j [string toupper [string index $hexvalue $i]]
      # Add it to the big string
        set total [string replace $total $start $start $j]
        incr start -1
    }
    set nlower [string range $total 8 15]
    set nupper [string range $total 0 7]
   # clear top bit to keep as positive. Also adds in "0x" at the start
   set nupper "[format "%#010X" [expr "0x$nupper" & "0x$mask"]]"
   # Now set to 64 bit - use a string to represent the number to avoid integer size limits
   set total "[expr [format "%u" "0x$nlower"] + (4294967295 * [format "%u" "$nupper"])]"
    return $total
}

proc uhex2dec32 {hexvalue} {
   # Creates an unsigned decimal number from a 32 bit hex value
   # Replace all non-hex characters
   regsub -all {[^0-9A-F\.\-]} $hexvalue {} newtemp
   set hexvalue [string trim $newtemp]
   #trim to 8 characters
   set hexvalue [string range $hexvalue [expr [string length $hexvalue]
- 8] [expr [string length $hexvalue] - 1]]
   return  [format "%#u" [expr "0x$hexvalue"]] } proc shex2dec32 {hexvalue} {
   # Creates a signed decimal number from a 32 bit hex value
   # Replace all non-hex characters
   regsub -all {[^0-9A-F\.\-]} $hexvalue {} newtemp
   set hexvalue [string trim $newtemp]
   #trim to 8 characters
   set hexvalue [string range $hexvalue [expr [string length $hexvalue]
- 8] [expr [string length $hexvalue] - 1]]
   return  [format "%#i" [expr "0x$hexvalue"]] }

proc uhex2dec16 {hexvalue} {
   # Creates an unsigned decimal number from a 16 bit hex value
   # Replace all non-hex characters
   regsub -all {[^0-9A-F\.\-]} $hexvalue {} newtemp
   set hexvalue [string trim $newtemp]
   #trim to 4 characters
   set hexvalue [string range $hexvalue [expr [string length $hexvalue]
- 4] [expr [string length $hexvalue] - 1]]
   set value [format "%#u" [expr "0x$hexvalue"]]
   return $value
}

proc shex2dec16 {hexvalue} {
   # Creates an unsigned decimal number from a 16 bit hex value
   # Replace all non-hex characters
   regsub -all {[^0-9A-F\.\-]} $hexvalue {} newtemp
   set hexvalue [string trim $newtemp]
   #trim to 4 characters
   set hexvalue [string range $hexvalue [expr [string length $hexvalue]
- 4] [expr [string length $hexvalue] - 1]]
   # Convert to signed number
   set value [format "%#u" [expr "0x$hexvalue"]]
   if {$value >  32767} {
      set value [expr ($value - 65536)]
   }
   return $value
}
