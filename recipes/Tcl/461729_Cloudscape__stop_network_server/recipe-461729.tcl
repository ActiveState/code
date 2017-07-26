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

======================================================================
# 
# stop cloudscape network server 

####################################################################
# Patrick Finnegan 17/11/2005.  V1. 
####################################################################

####################################################################
# Get Cloudscape connection.
####################################################################
proc stopServer { } {

   puts "\n**********"
   puts "Stop Server"
   puts "**********\n"

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

   puts "\nNetworkServerControl shutdown\n" 

   if { [ catch { $NetworkServerControl shutdown } r ] == 0 } {
   
        puts $r 

   } else {

        puts $r 
        return -code error

   }
}
####################################################################
# Main Control.
####################################################################

set computername [ lindex [ array get env COMPUTERNAME ] 1 ]

lappend optList "-Dderby.drda.host=$computername"
lappend optList "-Dderby.drda.portNumber=1527"

puts "\n java command line options list is:\n"

foreach x $optList {
    puts [ format "%-5s %-50s" " " $x ] 
}

set tclblend_init $optList  

#call java package 

package require java

set null [ java::null ]

if { [ catch { stopServer } r ] == 0 } {

    puts "\n Cloudscape Network Server on $computername shutdown successfully\n" 

} else {

    puts $r 
    exit 1   

}
