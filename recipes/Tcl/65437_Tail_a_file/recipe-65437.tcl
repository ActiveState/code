proc setup filename {
    text .t -width 60 -height 10 -yscrollcommand ".scroll set"
    scrollbar .scroll -command ".t yview"
    pack .scroll -side right -fill y
    pack .t -side left

    set ::fp [open $filename]
    seek $::fp 0 end
}

proc read_more {} {
    set new [read $::fp]
    if [string length $new] {
	.t insert end $new
	.t see end
    }
    after 1000 read_more
}

setup logfile
read_more

# Notice this is portable code.
# An industrial-strength version would probably exploit
#     namespaces ...
