#!/usr/local/bin/tcl
# fileevent/socket example

# Change the port to meet requirements.  Read it for example from the
# commandline or a configuration file

socket -server on_connect 18018

# Procedure called whenever a new connection is made by a client.
proc on_connect {newsock clientAddress clientPort} {

    # This is the place to add checks disallowing connections based
    # upon the hostname/ipaddress of the peer.

    fconfigure $newsock -blocking 0
    fileevent  $newsock readable [list handleInput $newsock]
}

# Procedure called whenever input arrives on a connection.
proc handleInput {f} {
    # Delete the handler if the input was exhausted.
    if {[eof $f]} {
        fileevent $f readable {}
        close     $f
        return
    }

    # Read and handle the incoming information. Here we just log it to
    # stdout.

    puts [read $f]
}
