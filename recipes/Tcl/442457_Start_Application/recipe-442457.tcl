#################################################################### 
# Start Enterprise Applications.
####################################################################
# Patrick Finnegan 01/09/2004.  V1. 
####################################################################
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 2} {

        set msg "error - not enough arguments supplied.  Supply application name and application server name"

        return -code error $msg
    
} 
######################################3
# set variables 
######################################3

set appServer [lindex $argv 0]
set app       [lindex $argv 1]

puts "*** AppServer   is $appServer ***"
puts "*** Application is $app ***"

# Assume one cell, one deployment manager node and one application node. 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodes  [ $AdminConfig list Node ]

# delete the manager node from the list.

set manIndex   [ lsearch -glob $nodes *Manager* ]
set nodeId     [ lindex [ lreplace $nodes $manIndex $manIndex ] 0 ]

# get name attribute for cell and application node

set cellName [ $AdminConfig showAttribute $cellId name ]
set nodeName [ $AdminConfig showAttribute $nodeId name ]

#######################################################################
# check whether the application is installed in the target app server.
#######################################################################

puts "\n *** checking if $app is installed *** \n " 

set apps [ $AdminApp list ]

puts "\n There are [ llength $apps ] installed applications:\n"

foreach i $apps { puts [ format "%-5s %-50s"  " "  $i ] }

puts "\n"

# if the application is installed and stopped, start the app.

if { [ lsearch -glob $apps $app ] == -1 } {

     puts " *** $app is not installed *** " 

} else {

   puts " *** checking if $app has started *** " 

   # "s" is not populated if the app is stopped 

   set s [ $AdminControl completeObjectName type=Application,name=$app,* ]

   if { [ string compare $s "" ] == 0 } {

       puts "\n *** starting $app *** \n" 

       # get app manager for the deployment manager.

       set appMan [ $AdminControl queryNames type=AppManagement,* ]

       set appList [ list $app null null ] 

       if { [ catch { $AdminControl invoke $appMan startApplication $appList } r ] == 0 } {

           puts "\n *** $app started successfully *** \n" 
	   puts "\n $r \n"

       } else {

	   return -code error $r

       }

   } else {

           puts "\n *** $app is already started *** \n" 

   }

}
