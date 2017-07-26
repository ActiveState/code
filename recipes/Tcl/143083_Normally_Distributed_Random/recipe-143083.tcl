# The following procedure generates two independent normally distributed 
# random numbers with mean 0 and vaviance stdDev^2.  If you only need 1
# random number, choose either one.

proc randNormal {stdDev} {
    global dRandNormal1
    global dRandNormal2

    set u1 rand()
    set u2 rand()

    set dRandNormal1 [expr $stdDev * sqrt(-2 * log($u1)) * cos(2 * 3.14159 * $u2)]
    set dRandNormal2 [expr $stdDev * sqrt(-2 * log($u1)) * sin(2 * 3.14159 * $u2)]
}

# The following code is only used to demonstrate the procedure and should
# be replaced by your own code.

for {set i 1} {$i<10} {incr i} {
	randNormal 1
	puts $dRandNormal1
	puts $dRandNormal2
}
