puts stdout "How many character long?"
set length [expr [gets stdin]+1]
puts stdout "Upper case characters too? y/n"
set upper [string toupper [gets stdin]]
set loop 1
set pass "generated pass="

proc random {range} {
    return [expr {round(rand()*$range)}]
}
# generate random number within given range

while {$loop != $length} {
	incr loop
	if {[random 4] == 1} { 
		append pass [format "%c" [expr [random 9]+48]] 
	} else { 
		set letter [format "%c" [expr [random 25]+97]] 
		if {$upper == "Y" && [random 1] } { 
			set letter [string toupper $letter]
		}	
		append pass $letter 
	}
}
# while there are still numbers to be appended.
# 1/4 chance a number is added to the string.
# 3/4 chance a letter is added to the string.
# 1/2 chance the letter is uppercased,
# provided the user has selected Y to uppercase

puts stdout "$pass"
