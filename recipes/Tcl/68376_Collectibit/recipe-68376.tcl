# bit.tcl --
#
#	Collection of bit manipulation functions.
#
# Copyright (c) 2000, 2001 by Scott Beasley.
#
namespace eval ::bit {
}

proc ::bit::testbit {bit_no flag} {
   return [expr {[expr {$flag & 1 << $bit_no}]?1:0}]
}

proc ::bit::setbit {bit_no in_flag} {
   upvar $in_flag flag
   set flag [expr {1 << $bit_no | $flag}]
}

proc ::bit::clearbit {bit_no in_flag} {
   upvar $in_flag flag
   set flag [expr {$flag ^ 1 << $bit_no}]
}

package provide bit 1.0

set TEST_PACKAGE 0

if {$TEST_PACKAGE} {
   # Test the Bit functions out.
   set flag 127
   set bit_no 7

   puts "flag value is $flag."
   ::bit::setbit $bit_no flag
   puts "bit_no $bit_no is [::bit::testbit $bit_no $flag]"

   puts "flag is now $flag."
   ::bit::clearbit $bit_no flag
   puts "bit_no $bit_no is [::bit::testbit $bit_no $flag]"
   puts "flag is now $flag."
}
