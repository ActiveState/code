# 
# Set activity log on.
#
####################################################################
# Patrick Finnegan 03/10/2005.  V1. 
####################################################################
proc setActivityLogOn { serverName } {

   puts "\n setActivityLogOn \n "

   global AdminConfig 

   set serverId            [ $AdminConfig getid /Server:$serverName/ ]

   set logServiceId        [ $AdminConfig list RASLoggingService $serverId ]  

   set messageFilterLevel  [ list messageFilterLevel WARNING ]

   set enableCorrelationId [ list enableCorrelationId true  ]
  
   set attrs               [ list $messageFilterLevel $enableCorrelationId ] 

   if { [ catch { $AdminConfig modify $logServiceId $attrs } r ] == 0 } {

       set serviceLogId [ $AdminConfig showAttribute $logServiceId serviceLog ] 

       set name    [ list name    D:/IBM/WebSphere/AppServer/logs/$serverName/activity.log ] 
       set size    [ list size    10    ]
       set enabled [ list enabled true  ]

       set attrs   [ list $name $size $enabled ]

       if { [ catch { $AdminConfig modify $serviceLogId $attrs } r ] == 0 } {

           set continue true

       } else {

	   puts $r
           return -code error

       }

   } else { 

       puts $r
       return -code error

   }

}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 1} {
        return -code error "error - no arguments supplied.  Supply server name"
        puts "no arguments"
}

# Assume one cell, one deployment manager node and one application node. 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodes  [ $AdminConfig list Node ]

# delete the manager node from the list.

set manIndex   [ lsearch -glob $nodes *Manager* ]
set nodeId     [ lindex [ lreplace $nodes $manIndex $manIndex ] 0 ]

# get name attribute for cell and application node

set cellName [ $AdminConfig showAttribute $cellId name ]
set nodeName [ $AdminConfig showAttribute $nodeId name ]

set serverName     [ lindex $argv 0 ]

puts "\nserver name    = $serverName\n"

####################################################################
# setActivityLogOn  
####################################################################

if { [ catch { setActivityLogOn $serverName } r ] == 0 } {
    puts "************************************"
    puts "Activity log settings applied successfully" 
    puts "************************************\n"
    puts "\n###### Admin Config Save ######\n"
    $AdminConfig save
} else {
        puts "\nFailed to apply Activity log settings. \n"
        puts $r 
        puts "************************************\n"
}
