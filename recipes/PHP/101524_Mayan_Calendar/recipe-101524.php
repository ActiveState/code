<?php

/**
 * JDToLongDate
 * $julianday is the julian day count, NOT a julian calendar date
 * $corresponder must be one of the numbers from the above list
 * returns a string containing a mayan day count
 */
function JDToLongDate($julianday,$corresponder){
	$JDA = $julianday - $corresponder;
        
	$bactuns = IntVal($JDA/144000);
        $JDA -= $bactuns * 144000;
        
	$katuns = IntVal($JDA/7200);
        $JDA -= $katuns * 7200;
        
	$tuns = IntVal($JDA/360);
        $JDA -= $tuns * 360;
        
	$uinals = IntVal($JDA/20);

        $kins = $JDA - ($uinals * 20);
	
	$longdate = "$bactuns.$katuns.$tuns.$uinals.$kins";
	
	return $longdate;
}

/**
 * LongDateToJD
 * $longdate is a mayan longdate as returned by JDToLongDate
 * $corresponder must be one of the numbers from the above list
 * returns a julian day count (NOT a julian calendar date)
 */
function LongDateToJD($longdate,$corresponder){
	list($bactuns,$katuns,$tuns,$uinals,$kins)=explode('.',$longdate);
	$daycount = ($bactuns * 144000) + ($katuns * 7200) + ($tuns * 360) + ($uinals * 20) + $kins;
	$julian = $daycount + $corresponder;
	return ($julian);
}


/* example usage */
$julian = GregorianToJD(12,31,2000);
$lc = JDToLongDate($julian,584283);
$jd = LongDateToJD($lc, 584283);
$date = JDToGregorian($jd);

echo "$lc = $date<br>\n";

// outputs 12.19.7.15.7 = 12/31/2000
?>
