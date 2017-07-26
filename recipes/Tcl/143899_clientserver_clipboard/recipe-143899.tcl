# client/server clipboard application
# ---------------------------------------------------
# (c) Stacom softwaredevelopment 2002
#  Freiburg, Germany, 
#  stacom@stacom-software.de
# ----------------------------------
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ----------------------------------
# Tested under:
# win NT 4.0 (client)
# Linix (server, client)
# ----------------------------------
# howto start:
# 1) configure server socket data
# 2) start server: >wish vmClip.tcl -server
# 3) start client: >wish vmClip.tcl -client <addrOfClient>
#
# hoto use
# select on client machine text 
# press send button of widget
# ...

namespace eval CNF {
    variable serverAdr "192.168.0.6"
    variable port "9010"
}

package require Tk

proc serverConnect {cid addr port} {
    puts "$cid: calling from $addr"
    fconfigure $cid -translation binary
    fileevent $cid readable "serverData  $cid"
}

proc serverData {cid} {
    puts "serverData: called from $cid [eof $cid]"
    if {[eof $cid]} {
        puts "client died ..."
        close $cid
    }
    set lLen [read $cid 4]
    binary scan $lLen "I" lLenStr
    if {[info exists lLenStr] == 0} {
        puts "client died ..."
        close $cid
        return
    }
    set lMsg [read $cid $lLenStr]
    showData $lMsg
    clipboard clear
    clipboard append $lMsg
}

proc showData {msg} {
    puts "show data:$msg"
    set lWn ".text"
    if {[string length $msg] == 0} {
        return
    }
    if {[winfo exists $lWn]} {
        destroy $lWn
    }
    set lText [text $lWn -width 30 -heigh 5 -wrap none]
    $lText insert end $msg
    pack $lText -fill both -expand yes
    wm title . vmClipboard
}

proc openClient {addr} {
    global gCltSock 
    wm geometry . +0+0
    if {[catch {set gCltSock [socket $addr $::CNF::port]} lErrMsg]} {
        error "error connecting to server ($lErrMsg)"
    }
    fconfigure $gCltSock  -translation binary
    button .b -command "sendText .t" -text "to $addr" -relief solid
    pack .b -side bottom
    wm title . "Clipboard $addr"
}

proc sendText {twidget} {
    global gCltSock
    set lRc [catch {set lClipboardContence [selection get -selection CLIPBOARD]}]
    if {$lRc} {
        return
    }
    set lMsg $lClipboardContence   
    set lDataToSend [binary format "I" [string length $lMsg] ]
    append lDataToSend $lMsg
    puts -nonewline $gCltSock $lDataToSend
    flush $gCltSock
}

# eval cmd line arguments
if {$argc == 0} {
    error "need cmd line -client or -server (got:$argv)"
} elseif {[lindex $argv 0] == "-client"} {
    set lServerAdr [lindex $argv 1]
    openClient $lServerAdr
} elseif {[lindex $argv 0] == "-server"} {
    set gServerSock [socket -server serverConnect -myaddr $::CNF::serverAdr $::CNF::port]
}
