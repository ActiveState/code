<?php

## Passing values to the commify() function
$number  = 100000;
$display_number = commify ($number);

## Display output
print "Input: $number" . "<br>"; 
print "Output: $display_number" . "<br>"; 

## The Commify Function
function commify ($str) { 
        $n = strlen($str); 
        if ($n <= 3) { 
                $return=$str;
        } 
        else { 
                $pre=substr($str,0,$n-3); 
                $post=substr($str,$n-3,3); 
                $pre=commify($pre); 
                $return="$pre,$post"; 
        }
        return($return); 
}

?>
