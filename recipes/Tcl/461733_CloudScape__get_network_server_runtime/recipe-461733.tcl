@echo off

setlocal

echo ###################################################
echo # Get Cloudscape runtime info on %computername%
echo ###################################################

set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derby.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbyclient.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbynet.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbytools.jar

set logFileDir=D:\CloudscapeDatabases\trace

d:\tclBlendSun\bin\jtclsh.bat D:\scripts\TCL\JACL\cloudscape\getRunTimeInfo.tcl %logFileDir%

endlocal

==========================================================================

# 
# get cloudscape runtime info on local host.

####################################################################
# Patrick Finnegan 24/11/2005.  V1. 
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
proc runtimeInfo { } {

   puts "\n**********"
   puts "runtimeInfo"
   puts "**********\n"

   global env 
   global null

   set hostName [ lindex [ array get env COMPUTERNAME ] 1 ]
   #set hostAddress [ java::call InetAddress getByName $hostName ]
   set hostAddress [ java::call InetAddress getByName "0.0.0.0" ]

   if { [ catch { java::new NetworkServerControl $hostAddress 1527 } r ] == 0 } {
   
        set NetworkServerControl $r 

   } else {

        return -code error $r

   }

   puts "\nget runtime info\n" 

   if { [ catch { $NetworkServerControl getRuntimeInfo } r ] == 0 } {

          puts  $r 

   } else {

        return -code error $r

   } 

   return $r

}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 1} {
        return -code error "\nerror - not enough arguments supplied.\nSupply log directory."
}

set computerName  $::env(COMPUTERNAME)
set traceDir      [ lindex $argv 0 ]
set traceFile     [ file join $traceDir runTimeInfo\.txt ]
set traceFileId   [ open $traceFile  w ]

set body         $traceFile

checkFile $traceDir

set header   "$computerName: get Cloudscape runtime info."
reportHeader $traceFileId $header $traceFile

set computerTime [clock format [clock seconds] -format "%d-%m-%Y %H.%M.%S"]

puts "tracefile = $traceFile" 

#call java package 

package require java

# import required classes 

java::import java.net.InetAddress
java::import org.apache.derby.drda.NetworkServerControl

puts "\nimported classes are:\n"

foreach i [java::import] {
   
  puts [ format "%-5s %-50s" " " $i ] 

}

set null [ java::null ]

if { [ catch { runtimeInfo } r ] == 0 } {

     lappend msg "\n********* Cloudscape Runtime Info *********\n"
     lappend msg $r

} else {

     lappend msg "\n********* Cloudscape Runtime Info Failed *********\n"
     lappend msg $r

} 

foreach i $msg {

    puts $i
    puts $traceFileId $i

}

close $traceFileId

set subject       "$computerName: Cloudscape Runtime Info."
set emailAddress  you@yourmail.com
sendSimpleMessage $emailAddress $subject $body
