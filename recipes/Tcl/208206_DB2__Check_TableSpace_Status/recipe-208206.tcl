#!d:\\Tcl\\bin\\tclsh84

######################################
# check db2 tablespaces
######################################

proc checkTablespace {userid password database} {

    package require textutil

    if {[catch {exec db2 connect to $database user $userid using $password} r] == 0} {
        set continue true
       } else {
	   return -code 1 [list $r]
    }

    set tableSpaces [exec db2 list tablespaces]
    set listed      [textutil::splitx $tableSpaces Tablespace]

    foreach list $listed {
        set r [lsearch -exact $list State]
	if {$r == -1} {
	    set continue true 
        } else {
	    if {[lindex $list [expr {$r + 2}]] == "0x0000"} {
		set status ok 
	    } else {
		lappend result_list $list
		set status notOK 
	    }
        }	
    }	

    exec db2 terminate
 
    if {$status == "ok"} {
       return 
    } else {
       return -code 1 $result_list
    }

}
