File: tcp_block.tcl
proc ClearMsgs { } {
   .fr_one.txt_log_msgs delete 1.0 end
}

proc block {port sock_hand client_ip client_port} {
   set cmd_data ""   
   set line "Access on port $port from IP $client_ip"
   if {$port == 80} {   
      set cmd_data " - [gets $sock_hand]"
   }
   
   close $sock_hand
   
   .fr_one.txt_log_msgs insert end "$line$cmd_data\n"
   .fr_one.txt_log_msgs see end   
}

# main ;-)

   wm title . {TCP Blocker}
   wm resizable . 0 0
   wm deiconify .

   frame .fr_one -borderwidth 0 -height 75 -relief groove -width 340 
   text .fr_one.txt_log_msgs -height 10 -state normal

   grid .fr_one -in . -column 0 -row 1 -columnspan 1 -rowspan 1 
   grid .fr_one.txt_log_msgs -in .fr_one -column 0 -row 2         -columnspan 1 -rowspan 1 

   frame .fr_two -borderwidth 0 -height 75 -relief groove -width 340 
   button .fr_two.b_clear -text "Clear" -command "ClearMsgs" -width 8           -state normal
   button .fr_two.b_quit -text "Quit" -command "set eot 1" -width 8           -state normal
   grid .fr_two -in . -column 0 -row 2 -columnspan 1 -rowspan 1 
   grid .fr_two.b_clear -in .fr_two -column 0         -row 1 -columnspan 1 -rowspan 1
   grid .fr_two.b_quit -in .fr_two -column 1         -row 1 -columnspan 1 -rowspan 1

   set port 1
   set eot 0

   # Get ports to Block.   
   source portstoblock

   foreach port [split $ports " "] {
      set sock_handles($port) [socket -server [list block $port] $port]
     .fr_one.txt_log_msgs insert end "Binding to $port\n"
   }      

   vwait eot

   foreach port $ports {
      puts $port      
      close $sock_handles($port)
   }      

   exit 0
   
# end main ;-)


File: portstoblock
set ports {21 22 23 25 42 43 53 80 109 110 111 119 143 443}
