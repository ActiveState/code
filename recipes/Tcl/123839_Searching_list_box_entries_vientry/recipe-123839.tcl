#initalize list box with dummy values

pack [ set lbox [listbox .lbox] ]

set name_list {"Carl Goode" "Rick Jones" "Tom Jones" "Ben Lewis" "Patti Oates" "Lisa Pelham" "Steve Smith" "Amy Taylor"}

foreach name $name_list {
    $lbox insert end $name
    #create list with index of value to search on
    lappend last_name_list [string tolower [lindex $name end]]
}

pack [frame .searchframe ]
    
label .searchframe.label -text "Search:"
set search_entry [entry  .searchframe.entry   -textvariable search_var -bg white]
set next_button  [button .searchframe.button -text "Next"]
bind $search_entry <KeyRelease> "SearchList $next_button $lbox [list $last_name_list]"

pack .searchframe.label $search_entry $next_button -side left

proc SearchList { next_button lbox last_name_list {old_index 0} } {
    global search_var
    
    set searchString [string tolower $search_var]
    set index [expr [lsearch -glob $last_name_list ${searchString}*] + $old_index]

    #Insure only one item is selected
    $lbox selection clear 0 end
    $lbox selection set $index
    $lbox selection anchor $index 
    
    $lbox see $index
    
    #update the name list for next button with items after most recent found
    set last_name_list  [list [lrange $last_name_list [incr index] end]]
    
    #Have a button to call procedure again with updated name list to view multiple entries.
    #Such as "Jones" in this example.
    $next_button configure -command "SearchList $next_button $lbox $last_name_list $index"
}
