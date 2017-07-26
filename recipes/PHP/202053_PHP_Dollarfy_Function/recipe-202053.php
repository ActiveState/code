<?php

## Passing values to the dollarfy() function
$Price = dollarfy (100000.1252, 2);

## Display output
print "output: $Price" . "<br>";

## Dollarfy Function
function dollarfy ($num,$dec) {
	 
	$format="%.$dec" . "f";  
        $number=sprintf($format,$num);
        $str=strtok($number,".");
        $dc=strtok(".");      
        $str=commify($str);
        $return="\$&nbsp;$str";

        if ($dec!=0) { 
                $return = "$return" . ".$dc";
        } 
        return($return); 
}

## Commify Function
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
