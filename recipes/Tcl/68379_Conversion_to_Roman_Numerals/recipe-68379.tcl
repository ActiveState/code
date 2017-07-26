proc toRoman {arabic} {
  #September 2001 by George M Jempty: jb4mt@webfielding.com
  
  if {![string is integer -strict $arabic] || $arabic < 1 || $arabic > 3999} {
    return -code error "Please retry with an integer from 1 to 3999"
  }
  
  set numerals [list I V X L C D M]
  set index 0
  set roman ""
  
  while {$arabic} {
    set digit [expr {$arabic%10}]
    set arabic [expr {$arabic/10}]
    set place ""

    if {$digit == 4 || $digit == 9} {
      set place [lindex $numerals [expr {$digit/4 + $index}]]
      set place [lindex $numerals $index]$place
    } else {
      for {set pad 0} {$pad < [expr {$digit%5}]} {incr pad} {
	set place [lindex $numerals $index]$place
      }
      if {$digit >= 5} {
        set place [lindex $numerals [expr {$index+1}]]$place
      }
    }
    incr index 2
    set roman $place$roman
  }  
  return $roman
}
