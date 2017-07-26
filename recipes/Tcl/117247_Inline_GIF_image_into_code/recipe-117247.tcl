package require base64 ; # in tcllib, part of ActiveTcl

proc inlineGIF {img {name ""}} {
    set f [open $img]
    fconfigure $f -translation binary
    set data [base64::encode [read $f]]
    close $f
    if {[llength [info level 0]] == 2} {
	# base name on root name of the image file
	set name [file root [file tail $img]]
    }
    return "image create photo [list $name] -data {\n$data\n}"
}
