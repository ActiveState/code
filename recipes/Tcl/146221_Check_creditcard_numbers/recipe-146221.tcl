# isluhn --
#   Checks whether a given number is a valid credit card number
# Mod 10 Rules					  
# The rules for a Mod 10 check: 			  
# The credit card number must be between 13 and 16 digits. 
#   The credit card number must start with: 	  
# 	  4 for Visa Cards 			  
# 	  37 for American Express Cards 		  
# 	  5 for MasterCards 			  
# 	  6 for Discover Cards 			  
#   If the credit card number is less then 16 digits add zeros to
#   the beginning to make it 16 digits.		  
#   Multiply each digit of the credit card number by the
#   corresponding digit of the mask, and sum the results together.
#   Once all the results are summed divide by 10, if there is no
#   remainder then the credit card number is valid.
# For a card with an even number of digits, double every odd numbered digit
# and substract 9 if the product is greater than 9. Add up all the even
# digits as well as the doubled odd digits, and the result must be a
# multiple of 10 or it's not a valid card. If a card has an odd number of
# digits, perform the same addition, doubling the even numbered digits
# instead...
# Arguments:
#   num		card num to check
# Results:
#   Returns 0/1
#
proc isluhn {cardnum} {
    regsub -all {[^0-9]} $cardnum {} cardnum
    #set cardnum [format %.16d $cardnum]
    set len [string length $cardnum]
    if {$len < 13 || $len > 16} { return 0 }
    set i -1
    set double [expr {!($len%2)}]
    set chksum 0
    while {[incr i]<$len} {
	set c [string index $cardnum $i]
	if {$double} {if {[incr c $c] >= 10} {incr c -9}}
	incr chksum $c
	set double [expr {!$double}]
    }
    return [expr {($chksum%10)==0}]
}
