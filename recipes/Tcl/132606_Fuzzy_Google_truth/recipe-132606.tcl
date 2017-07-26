#!/bin/sh
 # \
 exec wish "$0" "$@"
 package require http
 #http::config -proxyhost proxy -proxyport 80

 proc google'nhits query {
    set url  http://google.yahoo.com/bin/query?p=[string map {" " +} $query]&hc=0&hs=0
    set token [http::geturl $url]
    set data [http::data $token]
    http::cleanup $token
    set nhits 0
    regexp {\n[0-9-]+ of ([0-9]+)} $data -> nhits
    set nhits
 }
 proc go {w} {
    global query
    $w insert end "'$query': [google'nhits $query] hits\n"
 }
 entry .e -textvar query -bg white
 bind .e <Return> {go .t}
 text .t -bg white
 pack .e .t -fill x -expand 1
