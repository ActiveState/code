# int_bit_length_and_binary_repr.py
# Purpose: For integers from 0 to 256, print the number of 
# bits needed to represent them, and their values in binary.
# Author: Vasudev Ram
# Website: https://vasudevram.github.io
# Product store on Gumroad: https://gumroad.com/vasudevram
# Blog: https://jugad2.blogspot.com
# Twitter: @vasudevram

for an_int in range(0, 256 + 1):
    print an_int, "takes", an_int.bit_length(), "bits to represent,",
    print "and equals", bin(an_int), "in binary"
