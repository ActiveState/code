#
# cmpArray { a1 a2 }
#
# returns <list of indexes where there are differences>
#

proc cmpArray { ary1 ary2 } {
    upvar $ary1 a1
    upvar $ary2 a2

    set ilist1 [array names a1]
    set ilist2 [array names a2]

    foreach idx $ilist1 {
        # Make sure ary2 HAS this element!
        if {![info exists a2($idx)]} {
            # We don't have this element so...
            continue
        }

        if {$a1($idx) != $a2($idx)} {
            # They are not the same!
            lappend retn_list $idx
        }
    }

    if {![info exists retn_list]} {
        # There ARE no differences so return an empty list
        set retn_list [list {}]
    }

    return $retn_list
}
