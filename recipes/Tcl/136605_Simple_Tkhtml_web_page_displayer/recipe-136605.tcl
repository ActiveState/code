package require Tkhtml
package require http
pack [scrollbar .v -o v -co {.h yv}] -s right -f y
pack [html .h -ys {.v set}] -f both -e 1
bind .h.x <1> {eval g [.h href %x %y]}
proc g u {
    set t [http::geturl $u]
    .h cl
    .h p [http::data $t]
    http::cleanup $t
    .h co -base $u
}
g http://wiki.tcl.tk/976
proc bgerror args {}
# NEM :-)
