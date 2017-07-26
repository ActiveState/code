#!/bin/sh
#     exec tclsh "$0" ${1:+"$@"}
proc main {} {
    set fromchars ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    set tochars   NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm
    set map [list]
    foreach from [split $fromchars {}] to [split $tochars {}] {
        lappend map $from $to
    }
    puts stdout [string map $map [read stdin]]
}
main
