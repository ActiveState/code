proc shellsort args {
set key 0
set increment 3
foreach arg $args {
set numbers($key) $arg
incr key
}
set number [array size numbers]

while {$increment > 0} {
   for {set i 0} {$i < $number} {incr i} {
   set j $i
   set temp $numbers($i)

   while {($j >=$increment) && ($numbers([expr $j-$increment]) > $temp)} {
   set numbers($j) $numbers([expr $j - $increment])
   set j [expr $j - $increment]
   }
   set numbers($j) $temp
   }

if {[expr $increment/2] != 0} {
      set increment [expr $increment/2]
    } elseif {$increment == 1} {
      set increment 0
    } else {
      set increment 1
    }

}
for {set i 0} {$i < $number} {incr i} {
lappend sort $numbers($i)
}
puts $sort 
}

# Put the numbers after command separated with spaces
shellsort 
