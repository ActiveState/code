# 
# Set application profiling on.
#
####################################################################
# Patrick Finnegan 26/08/2004.  V1. 
####################################################################

proc setProfile { serverName } {

   global AdminConfig 

   set serverId [ $AdminConfig getid /Server:$serverName/ ]

   regexp {(.*)(\(cells.*)} $serverId 1 2 3
   set serverName $2

#  set JVM Properties. 

   if { [ catch { setJVMProps $serverId $serverName } r ] != 0 } {
	   return -code error $r
   }

#  set Process Definition Properties. 

   if { [ catch { setProcessDefProps $serverId $serverName } r ] != 0 } {
	   return -code error $r
   }

}
####################################################################
# Set JVM Properties.
####################################################################
proc setJVMProps {serverId serverName } {

   global AdminConfig 

   # get JVM id 

   set jvmId [ $AdminConfig list JavaVirtualMachine $serverId ]

   set existingGenericJvmArguments [$AdminConfig showAttribute $jvmId genericJvmArguments ]

   set msg "Current JVM genericJvmArguments are:"

   puts [ format "%-5s %s"  " " $msg  ]
       
   foreach i $existingGenericJvmArguments {

       puts [ format "%-10s %-40s"  " " $i ]

   }

   set arg1                   -XrunpiAgent
   set arg2                   -DPD_DT_ENABLED=true

   # the new generic arguments need to be appended to the existing args otherwise the existing args are overwritten. Check whether the arguments already exist.  If not merge the existing list with the new list.   
 
   if { [ lsearch $existingGenericJvmArguments "-XrunpiAgent" ] != -1 \
        || \
        [ lsearch $existingGenericJvmArguments "-DPD_DT_ENABLED=true" ] != -1 } {

       puts "do nothing"

   } else {

       set args                   [ list $arg1 $arg2 ]   

       set genericJvmArguments    [ list args ] 

       set genericJvmArguments    [ list genericJvmArguments [ concat $existingGenericJvmArguments $args ] ]

       set attrList [ list $genericJvmArguments ]

       if { [ catch { $AdminConfig modify $jvmId $attrList } r ] == 0 } {

	    set msg "New JVM genericJvmArguments are:"

	    puts [ format "%-5s %s"  " " $msg  ]

	    set genericJvmArguments [$AdminConfig showAttribute $jvmId genericJvmArguments ]

	    foreach i $genericJvmArguments {

		puts [ format "%-10s %-40s"  " " $i ]

	    }

	    puts "\n************************************"
	    puts "$serverName - JVM properties created successfully."
	    puts "************************************\n"
       } else {
	       puts "\nfailed to create Server JVM properties for $serverName\n"
	       puts "************************************\n"
	       return -code error $r
       }

   }

}
####################################################################
# Set Process Definition Properties.
####################################################################
proc setProcessDefProps {serverId serverName } {

   global AdminConfig 

   set processDefId [ $AdminConfig showAttribute $serverId processDefinition ]

   set existingExecutableArguments [$AdminConfig showAttribute $processDefId executableArguments]

   set msg "Current JVM Executable arguments are:"

   puts [ format "%-5s %s"  " " $msg  ]
       
   foreach i $existingExecutableArguments {

       puts [ format "%-10s %-40s"  " " $i ]

   }

   # the new generic arguments need to be appended to the existing args otherwise the existing args are overwritten. Check whether the arguments already exist.  If not merge the existing list with the new list.   
 
   if { [ lsearch $existingExecutableArguments "-XrunpiAgent" ] != -1 } {

       puts "do nothing"

   } else {

       set args                [ list -XrunpiAgent ] 

       set executableArguments [ list executableArguments [ eval concat $existingExecutableArguments $args ] ]

       set attrList [ list $executableArguments ]

       if { [ catch { $AdminConfig modify $processDefId $attrList } r ] == 0 } {

	    set executableArguments [$AdminConfig showAttribute $processDefId executableArguments]

	    set msg "New JVM Executable arguments are:"

	    puts [ format "%-5s %s"  " " $msg  ]
		
	    foreach i $executableArguments {

		puts [ format "%-10s %-40s"  " " $i ]

	    }

	    puts "\n************************************"
	    puts "$serverName - Process Definition properties created successfully."
	    puts "************************************\n"
       } else {
	       puts "\nfailed to create Process Definition properties for $serverName\n"
	       puts "************************************\n"
	       return -code error $r
       }

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
# setprofile  
####################################################################

if { [ catch { setProfile $serverName } r ] == 0 } {
    puts "************************************"
    puts "Profile set successfully"
    puts "************************************\n"
    puts "\n###### Admin Config Save ######\n"
    $AdminConfig save
} else {
        puts "\nFailed to apply profile settings\n"
        puts $r 
        puts "************************************\n"
}
