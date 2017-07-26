proc myProc {args} {
    set procName [lindex [info level 0] 0]
    puts "You called \"$procName\""
    puts "The full call was \"[info level 0]\""
}
