# Print columns
proc puts_tabular {width args} {
    set fmt [string repeat "%-${width}s" [llength $args]]
    puts [eval [list format $fmt] $args]
}
