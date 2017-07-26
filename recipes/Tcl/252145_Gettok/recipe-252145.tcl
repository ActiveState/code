proc gettok {1 2 3} {
 if {![string match -nocase *$3* $1]&&$2==1} {return $1}
 if {![string match -nocase *$3* $1]&&$2>1} {return}
 if {$2=="0"} {
  if {[string match -nocase *$3* $1]} {
   set a [split $1 $3];return [llength $a]
  };return 1
 }
 set a [split $1 $3];if {$2>[llength $a]} {return}
 if {[lindex $a [expr $2 - 1]]==""&&[lindex $a $2]!=""} {return [lindex $a $2]}
 return [lindex $a [expr $2 - 1]]
}
