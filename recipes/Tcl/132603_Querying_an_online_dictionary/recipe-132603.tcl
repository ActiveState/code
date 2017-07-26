--------------------------------------------------------------------------------

 package require http
 package require htmlparse
 package require ncgi
 namespace eval ::dict.leo.org {
    variable table ""
    proc parse {tag close options body} {
	variable TD
	variable table
	switch -- $close$tag {
	    TD     {set TD ""}
	    /TD    {if {[llength $TD]} {lappend table [string trim $TD]}}
	    default {append TD [string map {&nbsp; { }} $body]}
	}
    }
    proc query {query} {
	variable table
	set url "http://dict.leo.org/?search=[::ncgi::encode $query]"
	set tok [::http::geturl $url]
	foreach line [split [::http::data $tok] "\n"] {
	    if {[string match "*search results*" $line]} break
	}
	::http::cleanup $tok
	set table ""
	::htmlparse::parse -cmd ::dict.leo.org::parse $line
	return $table
    }
 }
 proc max {a b} {expr {$a > $b ? $a : $b}}
 proc main {argv} {
    set table [dict.leo.org::query [join $argv]]
    set max 0
    foreach c $table {set max [max $max [string length $c]]}
    set sep [string repeat = $max]
    set table [linsert $table 0 " English" " Deutsch" $sep $sep]
    foreach {c1 c2} $table {
	puts [format "%-*s  %-*s" $max $c1 $max $c2]
    }
    puts ""
 }
 main $argv
