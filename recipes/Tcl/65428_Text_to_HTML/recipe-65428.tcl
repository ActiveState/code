#!/usr/local/bin/tclsh
# -*- tcl -*-
# Scan the files in the current directory and wrap them into html/body
# tags so that netscape will display them as HTML and not as text.

foreach f [glob *] {
    if {[file extension $f] == ".html"} {continue}
    if {[file isdirectory $f]} {continue}
    set data [read [set fh [open $f r]]]
    close $fh
    set    fh [open html/$f.html w]
    puts  $fh "<html><body>\n$data</body></html>"
    close $fh
}
exit
