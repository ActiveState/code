@echo off

setlocal

echo ###################################################
echo # Start Cloudscape Server on %computername%
echo ###################################################

set derbyDir=D:\CloudscapeDatabases
set traceDir=D:\CloudscapeDatabases\trace

set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derby.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbyclient.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbynet.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbytools.jar

D:\scripts\TCL\JACL\cloudscape\startNetworkServer.tcl %derbyDir% %traceDir%

endlocal

=====================================================================

# 
# start cloudscape network server 

####################################################################
# Patrick Finnegan 17/11/2005.  V1. 
####################################################################

puts "\n **** executing [info script] **** \n"

# make script drive independent.

set drive [lindex [file split [info script]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

source $drive/scripts/TCL/proclib/checkFile_proc.tcl
source $drive/scripts/TCL/proclib/smtp_proc.tcl
source $drive/scripts/TCL/proclib/reportHeader_proc.tcl

####################################################################
# Get Cloudscape connection.
####################################################################
proc startServer { traceFile } {

   puts "\n**********"
   puts "startServer"
   puts "**********\n"

   global env 
   global null

   # import required classes 

   java::import java.net.InetAddress
   java::import org.apache.derby.drda.NetworkServerControl

   puts "\nimported classes are:\n"
   
   foreach i [java::import] {
       
      puts [ format "%-5s %-50s" " " $i ] 

   }

   if { [ catch { java::new NetworkServerControl } r ] == 0 } {
   
        set NetworkServerControl $r 

   } else {

        puts $r 
        return -code error

   }

   puts "\nNetworkServerControl start\n" 

   if { [ catch { $NetworkServerControl start $null } r ] == 0 } {

          puts  $r 
          puts  $traceFile $r 
          flush $traceFile 

   } else {

          puts "\n$r\n"
          puts $traceFile "\n$r\n"
          flush $traceFile 
          return -code error

   } 

   flush $traceFile 

   java::lock $NetworkServerControl

   return $NetworkServerControl

}
####################################################################
# Get Cloudscape server info.
####################################################################
proc serverInfo { traceFile NetworkServerControl } {

   puts "\n**********"
   puts "serverInfo"
   puts "**********\n"

   global env
   global null

   set hostName [ lindex [ array get env COMPUTERNAME ] 1 ]
   set hostAddress [ java::call InetAddress getByName "0.0.0.0" ]

   puts "\nNetworkServerControl ping\n" 

   if { [ catch { $NetworkServerControl ping } r ] == 0 } {

          puts  $r 
          puts  $traceFile $r 
          flush $traceFile 

   } else {

          puts "\n$r\n"
          puts $traceFile "\n$r\n"
          flush $traceFile 
          return -code error

   } 

   puts "\nNetworkServerControl getSysinfo\n" 

   if { [ catch { $NetworkServerControl getSysinfo } r ] == 0 } {

       puts  $r 
       puts  $traceFile $r 
       flush $traceFile 

   } else {

       puts "\n$r\n"
       puts $traceFile "\n$r\n"
       flush $traceFile 
       return -code error

   }

   puts "\nNetworkServerControl getRuntimeInfo\n" 

   if { [ catch { $NetworkServerControl getRuntimeInfo } r ] == 0 } {

       puts  $r 
       puts  $traceFile $r 
       flush $traceFile 

   } else {

       puts "\n$r\n"
       puts $traceFile "\n$r\n"
       flush $traceFile 
       return -code error

   }

   flush $traceFile 

}
####################################################################
# Ping Cloudscape Server.
####################################################################
proc pingServer { traceFile NetworkServerControl } {

   puts "\n**********"
   puts "pingServer"
   puts "**********\n"

   global null

   flush $traceFile 

   while {1} {

       after 30000
      
       puts "\n ping the server \n"

       if { [ catch { $NetworkServerControl ping } r ] == 0 } {

	   set s "[ clock format [ clock seconds ] ] NetworkServerControl ping ok "
	   puts  $s 
	   puts  $traceFile $s 
           flush $traceFile 

       } else {

	   puts "\n$r\n"
	   puts $traceFile "\n$r\n"
           flush $traceFile 
	   return -code error

       }

   flush $traceFile 

   }

}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 2} {

        return -code error "\nerror - not enough arguments supplied.\nSupply Derby dir and trace directory.\n"

}

set computerName  $::env(COMPUTERNAME)

set derbyDir      [ lindex $argv 0 ]
set traceDir      [ lindex $argv 1 ]
set traceFile     [ file join $traceDir traceFile\.txt ]
set traceFileId   [ open $traceFile  w ]

set body         $traceFile

checkFile $traceDir

set header   "$computerName: start Cloudscape Server"
reportHeader $traceFileId $header $traceFile

set computerTime [clock format [clock seconds] -format "%d-%m-%Y %H.%M.%S"]

puts "tracefile = $traceFile" 

# set database properties.

lappend optList "-Dderby.drda.host=$computerName"
# if configured to listen on the loopback address then will only accept connections from  local host. 
#lappend optList "-Dderby.drda.host=0.0.0.0"
lappend optList "-Dderby.drda.keepAlive=true"
lappend optList "-Dderby.infolog.append=true"
lappend optList "-Dderby.drda.logConnections=true"
lappend optList "-Dderby.drda.maxThreads=50"
lappend optList "-Dderby.drda.minThreads=10"
lappend optList "-Dderby.drda.portNumber=1527"
# start programatically rather then from property.
#lappend optList "-Dderby.drda.startNetworkServer=true"
lappend optList "-Dderby.drda.timeslice=2000"
lappend optList "-Dderby.drda.traceAll=true"
lappend optList "-Dderby.drda.traceDirectory=$traceDir"
lappend optList "-Dderby.system.home=$derbyDir"
#lappend optList "-Dderby.stream.error.logSeverityLevel=40000"
lappend optList "-Dderby.locks.monitor=true"
#lappend optList "-Dderby.locks.deadlockTrace=true"

puts "\n java command line options list is:\n"

foreach x $optList {
    puts [ format "%-5s %-50s" " " $x ] 
}

set tclblend_init $optList  

#call java package 

package require java

# build tcl classpath

set null [ java::null ]

if { [ catch { startServer $traceFileId  } r ] == 0 } {

    set NetworkServerControl $r

    if { [ catch { serverInfo $traceFileId $NetworkServerControl } r ] == 0 } {

       flush $traceFileId	
       set subject       "$computerName: Start Cloudscape Server"
       set emailAddress  youremail@you.com
       sendSimpleMessage $emailAddress $subject $body

       if { [ catch { pingServer $traceFileId $NetworkServerControl } r ] == 0 } {

	   set ok true

       }

    } 

} else {

    return

}


set computerTime [clock format [clock seconds] -format "%d-%m-%Y %H.%M.%S"]
puts $traceFileId "\n********* Cloudscape Server stopped at: $computerTime *********\n"
close $traceFileId

set subject       "$computerName: Cloudscape server Stopped."
set emailAddress  yourmail@yourmail.com
sendSimpleMessage $emailAddress $subject $body
