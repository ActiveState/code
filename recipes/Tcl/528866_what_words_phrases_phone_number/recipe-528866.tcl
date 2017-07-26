array set recode {
	1 {1}		2 {2 A B C}	3 {3 D E F}
	4 {4 G H I}	5 {5 J K L}	6 {6 M N O}
	7 {7 P Q R S}	8 {8 T U V}	9 {9 W X Y Z}
			0 {0}
}

set number {2 6 7 7 4 6 8}

set results {}
set temp {}
set is_first 1

foreach i $number {

	set temp_list [split $recode($i) " "]

	if {$is_first} {
		set is_first 0
		foreach j $temp_list {
			lappend results $j
		}
	} else {
		foreach item $results {
			foreach j $temp_list {
				lappend temp "$item$j"
			}
		}
		set results $temp
		set temp {}
	}
}

foreach item $results {
	puts $item
}
