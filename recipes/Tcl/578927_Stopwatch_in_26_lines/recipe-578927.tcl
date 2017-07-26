set seconds {}
set timetext 00:00:00
set id {}
ttk::label .time -textvariable timetext -font {Arial 32}
ttk::button .reset -text Reset -command reset
ttk::button .start -text Start -command {
    reset
    set seconds -1
    setSeconds
}
proc setSeconds {} {
    set ::id [after 1000 setSeconds]
    incr ::seconds
}
proc reset {} {
    if {$::id != {}} {
        after cancel $::id
    }
    set ::id {}
    set ::seconds 0
}
trace add variable seconds write updateTime
proc updateTime {args} {
    set ::timetext [clock format $::seconds -gmt 7 -format %H:%M:%S]
}
pack .time .reset .start
