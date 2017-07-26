# Shows how a server process can hand out task assignments 
# to related client processes. This is useful for distributing
# tasks of varying sizes amongst multiple CPUs on the same 
# host, or possibly multiple CPUs across many separate hosts.

# When a client is finished its current assignment, it will 
# ask the server for the next available task. This allows the
# server to distribute a group of tasks to make full use of
# the CPUs available. This avoids the issue of overloading
# one CPU while other CPUs are available but idle. The result
# is that a group of tasks is completed in the shorted possible
# elapsed real time.

# Written by John Brearley  Nov 2012.

# NB: On WinVista, early versions of TCL8.6 had issues of server
# socket not getting event notification of new client socket
# from same host. Fixed in TCL8.6B3. Never an issue on WinXP.

# Not yet tested on Linux or Win7 or higher.

# Parameters user might wish to customize
set child_timeout_sec 15 ;# Maximum time in seconds a child process is allowed for processing a file
set max_children 4 ;# maximum parallel running child processes allowed
set max_retry 3 ;# maximum times to try recovering from a error
set port_start 10500 ;# TCP port range to use
set port_end 10600

# Define list of dummy files to be processed by children processes.
# In a production script, you probably get list of filenames from
# a directory calling token.
# Files will be handed out for processing in the order specified.
# In case of error, it is assumed that a file can be reprocessed
# by itself, with no dependancies on other results.
set work_list "f1 f3 f6 f9 f2 f11 f12 f0 f4 f20 f19 f18 f30 f100 g1 g3 g6 g9 g2 g11 g12 g0 g4 g20 g19 g18 g30 g100 "

# ================ Common procs ==============================

# ================ check_child_timeout =======================
# If a child process is taking too long to process a file,
# closes the child socket to trigger reassignment of that file.
#
# Calling parameters: none
#
# Returns: null
# ============================================================
proc check_child_timeout { } {

   # Look for files started, but not finished yet.
   # puts "check_child_timeout processing"
   set now_sec [clock seconds]
   set timeout 0 ;# count number of timeouts this run
   for {set i 1} {$i <= $::work_max} {incr i} {
      set file $::work($i,file)
      set start $::work($i,start)
      set finish $::work($i,finish)
      # puts "check_child_timeout i=$i file=$file start=$start finish=$finish"
      # Skip files not started yet or already finished.
      if {$start == "" || $finish != ""} {
         # puts "check_child_timeout skipping i=$i file=$file start=$start finish=$finish"
         continue
      }

      # Has file been processing too long?
      set run_time [expr $now_sec - $start]
      if {$run_time > $::child_timeout_sec} {
         # An error will get logged when the socket is closed and cleaned up.
         # We DONT log an error here, so that there is only one error generated
         # for a single timeout, not two.
         incr timeout
         puts "check_child_timeout i=$i file=$file has run for $run_time seconds, taking recovery action."
         set ch_server $::work($i,ch_server)
         close_server_socket $ch_server TIME
      } else {
         # puts "check_child_timeout i=$i file=$file run_time=$run_time seconds OK"
      }
   }

   # May need to update the server.
   if {$timeout != 0} {
      update_server
   }
   # puts "check_child_timeout done"
   return
}


# ================ close_server_socket =======================
# Closes server socket, updates status with reason text.
#
# Calling parameters: channel reason
#
# Returns: null
# ============================================================
proc close_server_socket {ch reason} {

   # Close the socket, update the status.
   set reason [string toupper $reason]
   puts "close_server_socket ch=$ch reason=$reason"
   set catch_resp [catch "close $ch" catch_msg]
   if {$catch_resp == 0} {
      set ::socket_info($ch,status) "$reason Close OK"
   } else {
      set ::socket_info($ch,status) "$reason Close ERR"
      incr ::errors
      puts "close_server_socket ERROR: close $ch got: $catch_msg"
   }
   set ::socket_info($ch,finish) [clock seconds]

   # Need to clean up work array so any unfinished files associated
   # with this channel will be reassigned to new children.
   for {set i 1} {$i <= $::work_max} {incr i} {
      set ch_server $::work($i,ch_server)
      if {$ch != $ch_server} {
         # file is associated with different channel
         continue 
      }

      # This file is associated with the channel just closed.
      set finish $::work($i,finish)
      if {$finish != ""} {
         # file was completed OK
         continue 
      }

      set file $::work($i,file)
      set child_num $::work($i,child_num)
      set child_pid $::work($i,child_pid)
      puts "close_server_socket ERROR: $reason clean up for i=$i file=$file ch=$ch child_num=$child_num child_pid=$child_pid"
      incr ::errors
      # NB: DONT reset the try counter!
      set ::work($i,child_num) ""
      set ::work($i,child_pid) ""
      set ::work($i,ch_child) ""
      set ::work($i,ch_server) ""
      set ::work($i,start) ""
      set ::work($i,finish) ""
      set ::work($i,errors) 0
      set ::work($i,warnings) 0
   }
   return
}

# ================ display_socket_info =======================
# Displays available socket info collected by the server process.
#
# Calling parameters: server_port
#
# Returns: null
# ============================================================
proc display_socket_info {port} {

   # Show column titles
   puts "\ndisplay_socket_info server_port: $port"
   set f1 "%-9s %-13s %5s %-8s %5s %5s %-13s %5s %4s"
   puts "[format $f1 SrvSock ChHost ChPrt ChSock ChNum ChPID Status Delay Time]"
   puts "[format $f1 ======= ====== ===== ====== ===== ===== ====== ===== ====]"

   # Format data for each server channel.
   # Server channel is extracted from the chan,addr key pair
   set names [array names ::socket_info]
   set names [lsort $names]
   foreach item $names {
      # puts "display_socket_info item=$item"
      if {[regexp -nocase {(.*),addr} $item - chan]} {
         # puts "display_socket_info chan=$chan"
         set addr $::socket_info($chan,addr)
         set addr [lindex [split $addr ":"] end] ;# shorten IPV6 address
         set port $::socket_info($chan,port)
         set status $::socket_info($chan,status)
         set delay $::socket_info($chan,delay)
         if {$delay != "-"} {
            append delay ms
         }
         set ch_child $::socket_info($chan,ch_child)
         set child_num $::socket_info($chan,child_num)
         set child_pid $::socket_info($chan,child_pid)
         set start $::socket_info($chan,start)
         set finish $::socket_info($chan,finish)
         # set finish "" ;# test code
         if {[regexp {^\d+$} $start] && [regexp {^\d+$} $finish]} {
            set time [expr $finish - $start]
            append time s
         } else {
            set time "-"
         }
         puts "[format "$f1" $chan $addr $port $ch_child $child_num $child_pid $status $delay $time]"
      }
   }
   return
}

# ================ display_work_info =========================
# Displays available work info collected by the server process.
#
# Calling parameters: none
#
# Returns: null
# ============================================================
proc display_work_info { } {

   # Show column titles
   puts "\ndisplay_work_info"
   set f1 "%-16s %3s %5s %5s %-8s %-8s %4s %3s %4s"
   puts "[format $f1 Filename Try ChNum ChPID ChSock SrvSock Time Err Warn]"
   puts "[format $f1 ======== === ===== ===== ====== ======= ==== === ====]"

   # Format data for work item processed.
   for {set i 1} {$i <= $::work_max} {incr i} {
      set file $::work($i,file)
      set try $::work($i,try)
      set child_num $::work($i,child_num)
      set child_pid $::work($i,child_pid)
      set ch_child $::work($i,ch_child)
      set ch_server $::work($i,ch_server)
      set start $::work($i,start)
      set finish $::work($i,finish)
      if {[regexp {^\d+$} $start] && [regexp {^\d+$} $finish]} {
         set time [expr $finish - $start]
         append time s
      } else {
         set time "FAIL"
      }
      set errors $::work($i,errors)
      set warnings $::work($i,warnings)
      puts "[format "$f1" $file $try $child_num $child_pid $ch_child $ch_server $time $errors $warnings]"
   }
   return
}

# ================ launch_children ===========================
# Launch the children as independantly running parallel processes.
#
# Calling parameters: new_children host port
# new_children is an integer, the total number of new children
# to be created.
#
# Returns: null or throws error
# ============================================================
proc launch_children {new_children host port} {

   # Counter keeps track of how many times we launch children.
   if {![info exists ::child_launch_cnt]} {
      set ::child_launch_cnt 0 
   }
   incr ::child_launch_cnt

   # Counter is used to keep track of child numbers used.
   # The stdout information is easier to read when you keep
   # the child numbers unique. So we try to manage this value
   # automatically.
   if {![info exists ::current_child_max]} {
      # For server on remote host, we start child numbers at
      # a higher value. May or may not work out to be unique
      # depending on how many remote hosts access the same
      # server process
      if {$::host == $::local_host} {
         set ::current_child_max 0
      } else {
         set ::current_child_max [pid]
      }
   }
   incr ::current_child_max

   # Limit the number of new children launched at one time.
   if {$new_children > $::max_children} {
      set new_children $::max_children
   }
   set max_loop [expr $::current_child_max + $new_children - 1]
   puts "launch_children launching children $::current_child_max - $max_loop to $host:$port"

   # Launch the children
   for {set i $::current_child_max} {$i <= $max_loop} {incr i} {
      # $i is used as the child number to distinguish processes from each other.
      set ::current_child_max $i
      set catch_resp [catch "set pid \[eval exec tclsh $::argv0 $host $port $i &\]" catch_msg]
      if {$catch_resp == 0} {
         puts "launch_children launched child=$i pid=$pid"
      } else {
         error "launch_children ERROR: launching child=$i: $catch_msg"
      }
   }
   return
}

# ================ new_client ================================
# Procedure is called by vwait when new incoming client socket
# is received.
#
# Calling parameters: 3 arguments are supplied by vwait routine
#
# Returns: null
# ============================================================
proc new_client {new_ch new_addr new_port} {

   # Save newly assigned parameters
   save_new_client $new_ch $new_addr $new_port

   # Set up socket so it is non-blocking, and buffers a line.
   # If the socket is blocking (the default), then the server
   # can handle only 1 call at a time, which is interesting,
   # but not much practical use.
   fconfigure $new_ch -blocking 0 -buffering line -buffersize 100000

   # Set up file event handler. Script to execute, along with 
   # parameters, must be passed as a single string or list.
   # This allows the specifed routine to be run each time that
   # the socket has data ready to read.
   fileevent $new_ch readable "process_server_input $new_ch"

   # puts "\nserver: [fconfigure $new_ch]\n" ;# shows more data
   return
}

# ================ normal_child_exit =========================
# Normal exit routine for a child process.
#
# Calling parameters: child_num channel errors
#
# Returns: exits the child script
# ============================================================
proc normal_child_exit {child_num ch errors} {

   # Close the socket.
   set catch_resp [catch "close $ch" catch_msg]
   if {$catch_resp != 0} {
      incr errors
      puts "normal_child_exit ERROR: child_num=$child_num close $ch got: $catch_msg"
   }

   # Child process is done.
   puts "normal_child_exit child=$child_num ch=$ch errors=$errors time=[clock format [clock seconds] -format %H:%M:%S]"
   exit $errors
}

# ================ open_client_socket ========================
# Opens socket to specified host & port. Tries multiple times
# before giving up. 
#
# Calling parameters: host port child_num
# child_num is just for clarity in the messages
#
# Returns: socket_id or throws error
# ============================================================
proc open_client_socket {host port child_num} {

   # Define how often & how many times to try opening socket.
   set max_delay 3 ;# time in seconds between tries
   set max_tries 5

   # Open socket to server.
   for {set i 1} {$i <= $max_tries} {incr i} { 
      puts "open_client_socket host=$host port=$port child_num=$child_num Try #$i"
      set catch_resp [catch "set ch \[socket $host $port\]" catch_msg]
      if {$catch_resp == 0} {
         # Set the socket to non-blocking. This allows the gets loop
         # later on to get multiple lines of response from the server.
         fconfigure $ch -blocking 0
         puts "open_client_socket host=$host port=$port child_num=$child_num Try #$i OK ch=$ch"
         # puts "\nclient: [fconfigure $ch]\n" ;# shows more data
         return $ch

      } else {
         puts "open_client_socket host=$host port=$port child_num=$child_num Try #$i failed: $catch_msg"
         if {$i < $max_tries} {
            after [expr $max_delay * 1000]
         }
      }
   }
   error "open_client_socket ERROR: open socket to host=$host port=$port child_num=$child_num failed, tried $max_tries times, $catch_msg"
}

# ================ process_server_input ======================
# Called when fileevent indicates there is data on the
# specified channel to be read and processed. 
#
# Calling parameters: channel
#
# Returns: null
# ============================================================
proc process_server_input {ch} {

   # eof function checks for eof on channel.
   if {[eof $ch]} {  
      close_server_socket $ch EOF
      update_server
      return
   }

   # Get data from socket & parse.
   # Sequence numbers or strings are echoed back in response, as is.
   set input [string trim [gets $ch]] ;# read incoming data from socket
   set len [string length $input]
   set seq_num [string trim [lindex $input 0]]
   # test code to force sequence number error
   # if {[regexp {^\d+$} $seq_num]} {
   #    incr seq_num 
   # }
   set cmd [string tolower [lindex $input 1]]
   set args [lrange $input 2 end]
   # puts "process_server_input ch=$ch seq_num=$seq_num cmd=$cmd args=$args" ;# echo data to screen

   # Process cmd
   if {$input == ""} {
      # Ignore blank lines get OK response.
      # puts "process_server_input ch=$ch ignoring blank line"
      send_data process_server_input $ch "$seq_num OK"

   } elseif {$cmd == "child_info"} {
      # Children are expected to provide their details.
      set temp $::socket_info($ch,ch_child)
      # puts "process_server_input temp=$temp"
      if {$temp == ""} {
         # NB: null child info is caught later in request_work.
         puts "process_server_input registering seq_num=$seq_num cmd=$cmd args=$args ch=$ch"
         set ::socket_info($ch,ch_child) [lindex $args 0]
         set ::socket_info($ch,child_num) [lindex $args 1]
         set ::socket_info($ch,child_pid) [lindex $args 2]
         send_data process_server_input $ch "$seq_num OK"
      } else {
         incr ::errors
         send_data process_server_input $ch "$seq_num ERROR: already registered seq_num=$seq_num cmd=$cmd args=$args ch=$ch"
      }

   } elseif {$cmd == "request_work"} {
      eval request_work $ch $seq_num $args

   } elseif {$cmd == "work_done"} {
      eval work_done $ch $seq_num $args

   } else {
      # Unknown cmd ==> error
      incr ::errors
      send_data process_server_input $ch "$seq_num ERROR: unknown seq_num=$seq_num cmd=$cmd args=$args ch=$ch"
   }
   return
}

# ================ random_child_failure ======================
# This routine is used for testing error recovery. It creates
# random children failures. Do NOT call this routine in normal
# circumstances!
#
# Calling parameters: channel ch_num file
# These parameters are for ease of tracking log messages only.
# 
# Returns: null or exits script
# ============================================================
proc random_child_failure {ch ch_num file} {

   # For production script, should return immediately!
   # return 

   # 10% chance for process to exit.
   if {[expr rand()] <= 0.10} {
      puts "******** random_child_failure ch=$ch ch_num=$ch_num file=$file exiting ********"
      exit
   }

   # 10% chance for long delay / timeout
   if {[expr rand()] <= 0.10} {
      puts "******** random_child_failure ch=$ch ch_num=$ch_num file=$file sleeping ********"
      after 1000000000
   }
   return
}

# ================ request_work ==============================
# This routine finds the next task to be handed out to a child
# process. Sends work assignment to child process, or all_done.
#
# Calling parameters: ch seq_num args
# 
# Returns: null
# ============================================================
proc request_work {ch seq_num args} {
   # puts "request_work ch=$ch seq_num=$seq_num args=$args"
   
   # Is there any work to be done?
   set file ""
   set found ""
   for {set i 1} {$i <= $::work_max} {incr i} {
      set start $::work($i,start)
      set try $::work($i,try)
      if {($start == "") && ($try < $::max_retry)} {
         # This task needs to be (re)assigned.
         set found $i
         set file $::work($found,file)
         break
      }
   }

   # If no work left, send all done response.
   if {$found == ""} {
      send_data request_work $ch "$seq_num all_done seq_num=$seq_num args=$args"
      return
   }

   # Did the child register its info as expected?
   set cur_ch [lindex $args 0]
   set cur_num [lindex $args 1]
   set cur_pid [lindex $args 2]
   # puts "request_work cur_ch=$cur_ch cur_num=$cur_num cur_pid=$cur_pid"
   set reg_ch [string trim $::socket_info($ch,ch_child)]
   set reg_num [string trim $::socket_info($ch,child_num)]
   set reg_pid [string trim $::socket_info($ch,child_pid)]
   # puts "request_work reg_ch=$reg_ch reg_num=$reg_num reg_pid=$reg_pid"
   if {($reg_ch == "") || ($reg_num == "") || ($reg_pid == "")} {
      incr ::errors
      send_data request_work $ch "$seq_num ERROR: child info not registered, kicking child out, ch=$ch seq_num=$seq_num ch_chan=$cur_ch child_num=$cur_num child_pid=$cur_pid"
      after 100 ;# let child catch up
      close_server_socket $ch NOINFO
      update_server
      return
   }

   # Does child info in the current work request match the info already registered?
   if {($cur_ch != $reg_ch) || ($cur_num != $reg_num) || ($cur_pid != $reg_pid)} {
      incr ::errors
      send_data request_work $ch "$seq_num ERROR: child info mismatch: $cur_ch $cur_num $cur_pid NE $reg_ch $reg_num $reg_pid, seq_num=$seq_num"
      return
   }

   # Assign the found task to this child process.
   incr ::work($found,try)
   set ::work($found,child_num) $cur_num
   set ::work($found,child_pid) $cur_pid
   set ::work($found,ch_child) $cur_ch
   set ::work($found,ch_server) $ch
   set ::work($found,start) [clock seconds]
   send_data request_work $ch "$seq_num assigned_work file=$file try=$::work($found,try) assigned to ch=$ch ch_child=$cur_ch child_num=$cur_num child_pid=$cur_pid"
   return
}

# ================ save_new_client ===========================
# When recovering from errors and launching new clients, TCL 
# will happily reuse a socket name, assuming that the socket
# has been closed. When you try to keep track of socket info,
# this can lead to the older socket instance data being
# overwritten by the current socket instance data. So this
# routine will detect this condition and shuffle the older
# data into new entries in the ::socket_info array to preserve
# the older data.
#
# Calling parameters: new_ch new_addr new_port
#
# Returns: null
# ============================================================
proc save_new_client {new_ch new_addr new_port} {

   # Display newly assigned parameters
   puts "save_new_client new_ch=$new_ch new_addr=$new_addr new_port=$new_port"

   # Do we already have data for this channel?
   if {[info exists ::socket_info($new_ch,addr)]} {
      # Try to find an unused channel name.
      set found 0
      for {set i 1} {$i < 100} {incr i} {
         set temp "${i}${new_ch}"
         if {![info exists ::socket_info($temp,addr)]} {
            set found 1
            break
         }
      }

      # Move the older existing data to the unused channel name in array.
      if {$found == 0} {
         incr ::errors
         puts "save_new_client ERROR: socket $temp data will be overwritten!"
      }
      puts "save_new_client moving older $new_ch data to $temp"
      set ::socket_info($temp,addr) $::socket_info($new_ch,addr)
      set ::socket_info($temp,ch_child) $::socket_info($new_ch,ch_child)
      set ::socket_info($temp,child_num) $::socket_info($new_ch,child_num)
      set ::socket_info($temp,child_pid) $::socket_info($new_ch,child_pid)
      set ::socket_info($temp,port) $::socket_info($new_ch,port)
      set ::socket_info($temp,status) $::socket_info($new_ch,status)
      set ::socket_info($temp,delay) $::socket_info($new_ch,delay)
      set ::socket_info($temp,start) $::socket_info($new_ch,start)
      set ::socket_info($temp,finish) $::socket_info($new_ch,finish)
   }

   # Save the new client data
   set ::socket_info($new_ch,addr) $new_addr
   set ::socket_info($new_ch,ch_child) ""
   set ::socket_info($new_ch,child_num) ""
   set ::socket_info($new_ch,child_pid) ""
   set ::socket_info($new_ch,port) $new_port
   set ::socket_info($new_ch,status) ""
   set ::socket_info($new_ch,delay) "-"
   set ::socket_info($new_ch,start) [clock seconds]
   set ::socket_info($new_ch,finish) ""
   return
}

# ================ send_data =================================
# Routine sends data to specified socket, checks for errors.
#
# Calling parameters: calling_name channel data
# calling_name is for log info & error traceability.
#
# Returns: null or throws error
# ============================================================
proc send_data {calling_name ch data} {

   # Display info on terminal
   if {![regexp {OK$} $data]} {
      # Suppress routine OK only messages.
      puts "$calling_name $ch $data"
   }

   # Send data on channel, check for errors
   # set ch zzz ;# test code
   set catch_resp [catch "puts $ch \"$data\"" catch_msg]
   if {$catch_resp != 0} {
      error "ERROR: $calling_name $ch $data puts got: $catch_msg"
   }

   # Flush data, check for errors.
   # If you dont flush after each write, socket buffers data locally.
   # close $ch ;# test code
   set catch_resp [catch "flush $ch" catch_msg]
   if {$catch_resp != 0} {
      error "ERROR: $calling_name $ch $data flush got: $catch_msg"
   }
   return
}

# ================ send_server_get_resp ======================
# Sends request string to server, waits for server response.
#
# Calling parameters: channel seq_num request_string
#
# For enhanced error checking, the sequence number or id is sent
# at the start of the request to the sever. The server is
# expected to use this sequence number or id at the start of
# the response. If the response sequence number or id does
# NOT match that of the request, an error is thrown.
#
# Returns: response string from server, or throws error
# ============================================================
proc send_server_get_resp {ch seq_num request} {

   # Send sequence number and request to server.
   set start_ms [clock milliseconds] ;# milliseconds available in TCL8.5 and up
   send_data send_server_get_resp $ch "$seq_num $request"

   # Get server response and display it.
   # The response may be multiple lines.
   set max_sec 60 ;# timeout for getting response
   set start_sec [clock seconds]
   set response ""
   while {1} {
      # Check for timeout on socket
      after 50
      set now_sec [clock seconds]
      set delta [expr $now_sec - $start_sec]
      if {$delta >= $max_sec} {
         error "send_server_get_resp ERROR: timeout, waited $delta seconds for server response on ch=$ch seq_num=$seq_num request=$request"
      }

      # Collect data until we get some data followed by a null response.
      gets $ch data
      if {$response != "" && $data ==  ""} {
         break
      } else {
         append response $data
      }
   }

   # Validate response sequence number or id.
   # NB: lindex chokes on unmatched quotes in text string, so use regexp!
   # puts "send_server_get_resp seq_num=$seq_num response=$response"
   if {![regexp {^(.*?)\s} $response - response_seq]} {
      set response_seq "ERROR"
   }
   # puts "send_server_get_resp seq_num=$seq_num response_seq=$response_seq response=$response "
   if {$seq_num != $response_seq} {
      error "send_server_get_resp ERROR: sequence number $seq_num != $response_seq, request=$request response=$response"
   } 

   # Show results & timing.
   set stop_ms [clock milliseconds]
   set delta_ms [expr $stop_ms - $start_ms]
   if {$delta_ms > $::max_delay} {
      set ::max_delay $delta_ms
   }
   puts "send_server_get_resp ch=$ch seq_num=$seq_num request=$request response=$response delay=$delta_ms ms"
   return $response
}

# ================ start_server ==============================
# Starts the server listening process.
#
# Calling parameters: none
#
# Returns: TCP port number being listened to, or throws error
# ============================================================
proc start_server {} {

   # To allow for multiple server instances running on the same
   # host, we dynamically try to find an unused port number.
   # socket -server new_client $::port_start ;# test cod
   for {set port $::port_start} {$port <= $::port_end} {incr port} { 
      # Start server socket. It is here that we specify the routine
      # that we want to process incoming socket calls. In this case,
      # I have called the routine new_client.
      puts "start_server trying port $port"
      set catch_resp [catch "socket -server new_client $port" catch_msg]
      if {$catch_resp == 0} {
         puts "start_server listening on port $port, $catch_msg"
         return $port
      } else {
         puts "start_server port $port is not available, $catch_msg"
         after 500
      }
   }
   error "start_server ERROR: could not listen to any of ports $::port_start - $::port_end"
}

# ================ update_server =============================
# When all work is done, shuts down server. When necessary,
# starts more children processes.
#
# Calling parameters: none
#
# Returns: null
# ============================================================
proc update_server { } {

   # Is there any work left to do?
   set work_files ""
   set work_indices ""
   for {set i 1} {$i <= $::work_max} {incr i} {
      set file $::work($i,file)
      set finish $::work($i,finish)
      set try $::work($i,try)
      # puts "update_server i=$i file=$file finish=$finish try=$try"
      if {$finish == "" && $try < $::max_retry} {
         # This file is not finished yet, possibly not yet assigned either.
         lappend work_files $file
         lappend work_indices $i
      }
   }
   puts "update_server work_files=$work_files work_indices=$work_indices"

   # Are there any sockets still open?
   set sockets_open ""
   set names [array names ::socket_info]
   foreach item $names {
      # puts "update_server item=$item"
      if {[regexp -nocase {^(.*),addr$} $item - chan]} {
         set status $::socket_info($chan,status)
         # puts "update_server item=$item chan=$chan status=$status"
         if {![regexp -nocase {close} $status]} {
            # puts "update_server chan=$chan status=$status is still in use"
            lappend sockets_open $chan
         }
      }
   }
   puts "update_server sockets_open=$sockets_open"

   # When there is work to do and sockets are open, carry on. This is normal.
   if {$work_indices != "" && $sockets_open != ""} {
      puts "update_server keep working..."
      return
   }

   # When there is no work to do and sockets are still open, close the sockets.
   # Children should have done this themselves.
   if {$work_indices == "" && $sockets_open != ""} {
      puts "update_server no more work to do, closing sockets, shutting down server"
      foreach chan $sockets_open {
         close_server_socket $chan DONE
      }
      set ::doneit shutdown ;# vwait will recognize the variable has been updated
      return
   }

   # When there is no work and all sockets are closed. This is the expected
   # normal end. Trigger vwait to end the server process.
   if {$work_indices == "" && $sockets_open == ""} {
      puts "update_server no more work to do, all channels are closed, shutting down server"
      set ::doneit shutdown ;# vwait will recognize the variable has been updated
      return
   }

   # Oops! There are no sockets, but we still have work to do!!!
   # Have we already hit this error?
   if {$::child_launch_cnt < $::max_retry} {
      # Launch more children
      after 1000 ;# dont be too aggressive
      incr ::errors
      puts "update_server ERROR: No sockets open, but we still have work to do: $work_files"
      set cnt [llength $work_indices]
      launch_children $cnt $::host $::port
      return

   } else {
      incr ::errors
      puts "update_server ERROR: launched children $::child_launch_cnt times already, shutting server down!"
      set ::doneit shutdown ;# vwait will recognize the variable has been updated
      return
   }
}

# ================ work_done =================================
# This routine logs the results of processing a specific task.
#
# Calling parameters: ch seq_num args
# args can include optional error & warning counts from
# processing the specific file. These are added to the server
# running totals. 
# 
# Returns: null
# ============================================================
proc work_done {ch seq_num args} {
   # puts "work_done ch=$ch seq_num=$seq_num args=$args"
   
   # Parse calling data
   set cur_ch [lindex $args 0]
   set cur_num [lindex $args 1]
   set cur_pid [lindex $args 2]
   set cur_file [lindex $args 3]
   set cur_delay [lindex $args 4]
   set cur_err [lindex $args 5] ;# optional
   set cur_warn [lindex $args 6] ;# optional
   # puts "work_done cur_ch=$cur_ch cur_num=$cur_num cur_pid=$cur_pid cur_file=$cur_file cur_delay=$cur_delay cur_err=$cur_err cur_warn=$cur_warn"

   # Get work data for file being reported as done processing.
   set found ""
   for {set i 1} {$i <= $::work_max} {incr i} {
      set work_file $::work($i,file)
      if {$work_file == $cur_file} {
         # Valid file, get more data
         set found $i
         set work_ch_child $::work($found,ch_child)
         set work_ch_server $::work($found,ch_server)
         set work_child_num $::work($found,child_num)
         set work_child_pid $::work($found,child_pid)
         set work_finish $::work($found,finish)
         break
      }
   }

   # File not found => error.
   if {$found == ""} {
      incr ::errors
      send_data work_done $ch "$seq_num ERROR: file=$cur_file not in work list, ch=$ch seq_num=$seq_num args=$args"
      return
   }

   # Verify work being reported on was assigned to this child.
   if {($ch != $work_ch_server) || ($cur_ch != $work_ch_child) || ($cur_num != $work_child_num) || ($cur_pid != $work_child_pid)} {
      incr ::errors
      send_data work_done $ch "$seq_num ERROR: file=$cur_file work assignment mismatch: $ch $cur_ch $cur_num $cur_pid NE $work_ch_server $work_ch_child $work_child_num $work_child_pid seq_num=$seq_num"
      return
   }

   # Verify work has not already been reported on.
   if {$work_finish != ""} {
      incr ::errors
      send_data work_done $ch "$seq_num ERROR: file=$cur_file assignment already reported done: ch=$ch seq_num=$seq_num args=$args"
      return
   }

   # This is a valid work done report. Log the finish time.
   set ::work($found,finish) [clock seconds]

   # Delay stats are now collected as part of each work done report.
   # This avoids race conditions where both the server & children 
   # processes exit and some delay stats get lost in flight.
   set ::socket_info($ch,delay) $cur_delay

   # Log optional errors & warnings
   if {[regexp {^\d+$} $cur_err] && $cur_err > 0} {
      incr ::errors $cur_err
      puts "work_done ERROR: file=$cur_file reported $cur_err errors"
      set ::work($found,errors) $cur_err
   }
   if {[regexp {^\d+$} $cur_warn] && $cur_warn > 0} {
      incr ::warnings $cur_warn
      puts "work_done WARNING: file=$cur_file reported $cur_warn warnings"
      set ::work($found,warnings) $cur_warn
   }

   # Send response.
   send_data work_done $ch "$seq_num OK ch=$ch seq_num=$seq_num args=$args"
   return
}

# ============================================================
# Main program
# ============================================================
# Initialization
set errors 0
set local_host [exec hostname] ;# Works on Windows & Linux
set max_delay 0 ;# tracks max server response time, in milliseconds
set self [file root [file tail $::argv0]]
set warnings 0

# Online help
set x [lindex $argv 0]
set x [string range $x 0 1]
set x [string tolower $x]
# puts "x=$x"
if {$x == "-h" || $x == "/?"} {
   puts "Basic usage: $self \[host\] \[port\]"
   puts " "
   puts "Demo of task load balancing between processes on"
   puts "multiple CPUs."
   puts " " 
   puts "By default, host is localhost and port is $port_start."
   puts "port is only used when accessing server on a remote host."
   exit 1
}

# Get command line tokens
set host [string tolower [string trim [lindex $argv 0]]]
if {$host == "" || $host == "localhost"} {
   set host $local_host
}
set port [string tolower [string trim [lindex $argv 1]]]
if {$port == ""} {
   set port $port_start
}
# Child_num distinguishes child process from server process.
set child_num [string tolower [string trim [lindex $argv 2]]]
# puts "main host=$host port=$port child_num=$child_num"

# Child code goes here.
if {$child_num != ""} {

   # Open socket to server
   set ch [open_client_socket $host $port $child_num]

   # Sequence numbers on transactions are used for enhanced error checking.
   # Usually numeric, could be alpha string. Key point is to be unique.
   # If sequence number is not unique, then enhanced error cheking is defeated.
   set seq_num 0

   # Send child info to server
   incr seq_num
   set child_pid [pid]
   set child_info "$ch $child_num $child_pid"
   send_server_get_resp $ch $seq_num "child_info $child_info"

   # Process work assigned by server process.
   while { 1 } {

      # Ask server for next assigned task
      incr seq_num
      set server_resp [send_server_get_resp $ch $seq_num "request_work $child_info"]
      set resp [lindex $server_resp 1] ;# NB: token 0 is seq_num
      set file [lindex [split [lindex $server_resp 2] "="] end] ;# token is formated: file=name
      # puts "child_num=$child_num resp=$resp file=$file"
      if {$resp == "all_done"} {
         puts "child_num=$child_num got $resp"
         break ;# thats it, nothing more to do.
      }
      if {$resp == "ERROR:" || $file == ""} {
         incr errors
         puts "ERROR: child_num=$child_num got resp=$resp file=$file"
         break ;# exit due to errors.
      }

      # For testing purposes only, add random errors & timeouts to simulation.
      # Do NOT call this routine in a production script!
      random_child_failure $ch $child_num $file

      # This is where the real processing would be done. 
      # Could be a call to external routine or TCL packages.
      set delay [expr int(rand()*10)]
      puts "child=$child_num delay=$delay sec ch=$ch file=$file"
      after [expr $delay * 1000]

      # Tell server we are done with this assignment.
      # We can pass back optional error & warning counts for the server to collate.
      set err 0
      set warn 0
      incr seq_num
      send_server_get_resp $ch $seq_num "work_done $child_info $file $max_delay $err $warn"
   }

   # Child process is now done.
   normal_child_exit $child_num $ch $errors
}

# Remaining code is run only by the server process.

# Start server when running on localhost.
# Server port will override the command line port.
if {$host == $local_host} {
   set port [start_server]
   puts "main port=$port"

   # Set up work_list array for servers use.
   set work_max 0
   foreach file $work_list {
      incr work_max
      set work($work_max,file) $file ;# filename to be processed
      set work($work_max,try) 0 ;# counter to track how many times file has been assigned
      set work($work_max,child_num) "" ;# child number assigned to process this file
      set work($work_max,child_pid) "" ;# child process id assigned to process this file
      set work($work_max,ch_child) "" ;# child channel assigned to process this file
      set work($work_max,ch_server) "" ;# server channel assigned to process this file
      set work($work_max,start) "" ;# start time, in seconds, that task was assigned
      set work($work_max,finish) "" ;# finish time, in seconds, that task was reported finished
      set work($work_max,errors) 0 ;# child processing code may report an error count
      set work($work_max,warnings) 0 ;# child processing code may report a warning count
   }
   puts "main work_max=$work_max"
   # display_work_info
}

# Launch the children as independantly running parallel processes.
launch_children $max_children $host $port
if {$host != $local_host} {
   puts "$self main children will keep running..."
   exit
}

# Create dummy variable for vwait to watch.
set doneit "running"  
# puts "main doneit=$doneit"

# Set child timeout poll timer to 1/10 of child_timeout_sec.
set poll_ms [expr int($child_timeout_sec * 1000 / 10 )]

# Vwait processes socket events until dummy variable doneit is updated.
puts "main starting vwait..."
while {$doneit != "shutdown" } {

   # Set the periodic timer so we are guaranteed to be able to go check
   # for children timeouts. 
   after $poll_ms {set doneit check}

   # Let vwait handle socket events.
   vwait doneit

   # When the periodic timer has kicked, go look for children taking too long.
   if {$doneit == "check"} {
      check_child_timeout
      # NB: update_server may alter value of doneit, so be careful here!
      if {$doneit == "check"} {
         set doneit running
      }
   }
}
puts "main vwait finished doneit=$doneit"

# Trace info
after 1000
display_socket_info $port
display_work_info

# Thats it, we are done.
puts "\n$self main all done, $errors errors, $warnings warnings."
exit $errors
