#!/usr/local/bin/tclsh
#
# PFW - Portforwarder tcltk use at own risk, Norman Deppenbroek 2001
#
# forwarding raw data from a listening port, towards a standard remote address:port
# block by session limits and accesslist
#


namespace eval pfw {

        variable version        v0.93
        variable copyright      "PortForwarder $pfw::version by Nodep"
        variable debug          False	# if true show packet size on stdout 
        variable localhost      0
        variable localport      0
        variable remotehost     0
        variable remoteport     0
        variable maxsession     0
        variable allowlist      0
        variable denylist       0


        proc time  {}           { return [ clock format [ clock seconds ] -format %D-%T ] }
        proc print { syntax }   { puts "[ pfw::time ] --> $syntax" }
                
                namespace eval db {
                        variable cnt 0    

                        proc inc { } {
                                return [ incr pfw::db::cnt ]
                        }

                        proc dec { } {
                                return [ set pfw::db::cnt [ expr $pfw::db::cnt - 1 ] ]
                        }
                
                }
}


 
# PROCEDURES START HERE #

proc sio { fromsock tosock ip port } {
        
         if { [ catch { set data [read $fromsock] } merror ] } {
                pfw::print "ERR: #$pfw::db::cnt \t $merror"
                pfw::print "CLR: #$pfw::db::cnt \t $pfw::remotehost:$pfw::remoteport <-> $pfw::localhost:$pfw::localport <-> $ip:$port"
                catch { close $fromsock } 
                catch { close $tosock   } 
                pfw::db::dec
                return
         }


          if {[string length $data] == 0} {

                catch { close $fromsock }
                catch { close $tosock }  
                pfw::print "CLR: #$pfw::db::cnt \t $pfw::localhost:$pfw::localport <-> $pfw::remotehost:$pfw::remoteport <->  $ip:$port"
                pfw::db::dec
                return      
          }
                if { $pfw::debug } { pfw::print "TRX: #$pfw::db::cnt \t $pfw::remotehost:$pfw::remoteport <-> $pfw::localhost:$pfw::localport

                if { [ catch { puts -nonewline $tosock $data } merror ] } {
                        pfw::print "ERR: #$pfw::db::cnt \t $merror"
                        pfw::print "CLR: #$pfw::db::cnt \t $pfw::remotehost:$pfw::remoteport <-> $pfw::localhost:$pfw::localport <-> $ip:$port
                        catch { close $fromsock }
                        catch { close $tosock }  
                        pfw::db::dec
                }
}
 
 
proc connect { serverhost serverport sockclient ip port} {

        pfw::db::inc

        if { $pfw::db::cnt < $pfw::maxsession } {

           if { [ lsearch -exact $pfw::allowlist $ip ] != -1 } {

                  if { [ catch { set sockserver [ socket $pfw::remotehost $pfw::remoteport ] } merror ] } {
                        pfw::print "ERR: #$pfw::db::cnt \t $merror"
                        pfw::print "CLR: #$pfw::db::cnt \t $pfw::localhost:$pfw::localport <-> $ip:$port"
                        catch { close $sockclient }
                        catch { close $sockserver }
                        pfw::db::dec
                        return
                  }

                  pfw::print "NEW: #$pfw::db::cnt \t $pfw::localhost:$pfw::localport <-> $ip:$port" 
                  pfw::print "CON: #$pfw::db::cnt \t $pfw::localhost:$pfw::localport <-> $ip:$port "
                  fconfigure $sockclient -blocking 0 -buffering none -translation binary 
                  fconfigure $sockserver -blocking 0 -buffering none -translation binary 
                  fileevent  $sockclient  readable [list sio $sockclient $sockserver $ip $port ]
                  fileevent  $sockserver  readable [list sio $sockserver $sockclient $ip $port ]

          } else {

                  pfw::print "INT: #$pfw::db::cnt \t $ip:$port rejected by accesslist!"
                  catch { close $sockclient }
                  pfw::db::dec

          }


        } else {

                pfw::print "INT: #$pfw::db::cnt \t $ip:$port rejected, maxsession reached!"
                catch { close $sockclient }
                pfw::db::dec
        }
 
}

# MAIN STARTS HERE #

if { $argc == 7 } {

                set pfw::db::cnt        0
                set pfw::localhost      [ lindex $argv 0 ]
                set pfw::localport      [ lindex $argv 1 ]
                set pfw::remotehost     [ lindex $argv 2 ]
                set pfw::remoteport     [ lindex $argv 3 ]
                set pfw::maxsession     [ lindex $argv 4 ]
                set pfw::debug          [ lindex $argv 5 ]

                if { [ catch { set infile [ open [ lindex $argv 6 ]] } merror ] } {
                        puts "ERROR - $merror"
                        exit

                } else {

                        set pfw::allowlist [ read $infile ]
                        if { [ catch { close $infile } merror ] } {
                                puts "ERROR - $merror"
                                exit
                        } 
                }
                 
                pfw::print "---------------------------------------------------------------------------------------"
                pfw::print "$pfw::copyright - $pfw::localhost:$pfw::localport <-> $pfw::remotehost:$pfw::remoteport"
                pfw::print "Allowing connections from:"
                for {set x 0} { $x < [ llength $pfw::allowlist ]} {incr x} {pfw::print [ lindex $pfw::allowlist $x ] }
                pfw::print "---------------------------------------------------------------------------------------"  
                socket -server [list connect $pfw::remotehost $pfw::remoteport ] -myaddr $pfw::localhost $pfw::localport
                vwait forever

} else {

        puts "\n\n"
        puts "------------------------------------"
        puts "$pfw::copyright - Usage:"
        puts "------------------------------------"
        puts "$argv0 localhost localport remotehost remoteport maxsessions false|true xslist.pfw\n\n"
}
 




# make a file called xslist.pfw and store it in de directory where pfw.tcl
# is listed and executed. XSLIST.PFW contains 1 line of allowed ip addresses:
127.0.0.1 192.168.168.110 212.121.221.121 192.168.168.120 192.168.168.12
