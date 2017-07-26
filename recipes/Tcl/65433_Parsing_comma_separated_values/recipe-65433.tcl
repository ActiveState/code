proc csv2list {str {sepChar ,}} {
    regsub -all {(\A\"|\"\Z)} $str \0 str
    set str [string map [list $sepChar\"\"\" $sepChar\0\" 		\"\"\"$sepChar \"\0$sepChar 		\"\" \" \" \0 ] $str]
    set end 0
    while {[regexp -indices -start $end {(\0)[^\0]*(\0)} 		$str -&gt; start end]} {
	set start [lindex $start 0]
	set end   [lindex $end 0]
	set range [string range $str $start $end]
	set first [string first $sepChar $range]
	if {$first &gt;= 0} {
	    set str [string replace $str $start $end 		[string map [list $sepChar \1] $range]]
        }
        incr end
    }
    set str [string map [list $sepChar \0 \1 $sepChar \0 {} ] $str] 
    return [split $str \0]
}


proc list2csv {list {sepChar ,}} {
    set out ""
    foreach l $list {
	set sep {}
	foreach val $l {
	    if {[string match "*\[\"$sepChar\]*" $val]} {
		append out $sep\"[string map [list \" \"\"] $val]\"
            } else {
		append out $sep$val
	    }
	    set sep $sepChar
	}
	append out \n
    }
    return $out
}
