# 
# Set performance monitoring service on.
# Set performance monitoring flags. 
#
####################################################################
# Patrick Finnegan 28/09/2005.  V1. 
####################################################################
proc setPerMonOn { serverName } {

   puts "\n setPerMonOn \n "

   global AdminConfig 

   set serverId       [ $AdminConfig getid /Server:$serverName/ ]

   set PMIServiceList [ $AdminConfig list PMIService ]  
 
   # get PMI service object for target server 

   set serverIndex      [ lsearch -glob $PMIServiceList *$serverName* ]

   set PMIServiceId     [ lindex $PMIServiceList $serverIndex ] 

   set enable           [ $AdminConfig showAttribute $PMIServiceId enable ]

   set initialSpecLevel [ $AdminConfig showAttribute $PMIServiceId initialSpecLevel ]

   set msg "Current Performance Monitor Settings Spec level:\n"

   puts [ format "%-5s %s"  " " $msg  ]
       
   puts [ format "%-10s %-20s %-40s"  " " enable           $enable ]
   puts [ format "%-10s %-20s %-40s"  " " initialSpecLevel $initialSpecLevel ]

   set enable              [ list enable true ]

   append X beanModule=X: 
   append X acheModule=X:
   append X connectionPoolModule=X:
   append X j2cModule=X:
   append X jvmRuntimeModule=X:
   append X orbPerfModule=X:
   append X servletSessionsModule=X:
   append X systemModule=X:
   append X threadPoolModule=X:
   append X transactionModule=X:
   append X webAppModule=X:
   append X wlmModule=X:
   append X webServicesModule=X:
   append X wsgwModule=X:

   set initialSpecLevel   [ list initialSpecLevel $X ]

   set attrsList          [ list $enable $initialSpecLevel ]	

   if { [ catch { $AdminConfig modify $PMIServiceId $attrsList } r ] == 0 } {

       set enable           [ $AdminConfig showAttribute $PMIServiceId enable ]
       set initialSpecLevel [ $AdminConfig showAttribute $PMIServiceId initialSpecLevel ]

       set msg "New Performance Monitor Settings Spec level:"

       puts [ format "%-5s %s"  " " $msg  ]
	   
       puts [ format "%-10s %-20s %-40s"  " " enable           $enable ]
       puts [ format "%-10s %-20s %-40s"  " " initialSpecLevel $initialSpecLevel ]


       if { [ catch { setJVMProps $serverName } r ] == 0 } {

           setRunPerfAdvisor $serverName 
	   #puts $r

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
# Set JVM Properties.
####################################################################
proc setJVMProps { serverName } {

   global AdminConfig 

   set serverId       [ $AdminConfig getid /Server:$serverName/ ]

   # get JVM id 

   set jvmId [ $AdminConfig list JavaVirtualMachine $serverId ]

   # get existing arguments  

   set existingGenericJvmArguments [$AdminConfig showAttribute $jvmId genericJvmArguments ]

   set msg "Current JVM genericJvmArguments are:"

   puts [ format "%-5s %s"  " " $msg  ]
       
   foreach i $existingGenericJvmArguments {

       puts [ format "%-10s %-40s"  " " $i ]

   }

   # the new generic arguments need to be appended to the existing args otherwise the existing args are overwritten. Check whether the arguments already exist.  If not merge the existing list with the new list.   
 
   if { [ lsearch $existingGenericJvmArguments "-XrunpmiJvmpiProfiler" ] != -1 } {

       #puts "do nothing"
       set continue true 

   } else {

       set args                   [ list -XrunpmiJvmpiProfiler ] 

       # use eval concat to trim spaces.
       set genericJvmArguments    [ list genericJvmArguments [ eval concat $existingGenericJvmArguments $args ] ]

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
# Enable Runtime Performance Advisor.
# NB - server must be running to pick up MBean.
####################################################################
proc setRunPerfAdvisor { serverName } {

   puts "\n setRunPerfAdvisor \n "

   global AdminConfig 
   global AdminControl 

   set perfId [ $AdminControl queryNames mbeanIdentifier=ServerRuleDriverMBean,process=$serverName,*]

   # if the server is not running the mbean will be null. 

   if { [ string length $perfId ] != 0 } {
       
       # get existing arguments  

       set enabled [ $AdminControl getAttribute $perfId enabled ]

       puts "\nCurrent RPA Status is: $enabled\n " 

       $AdminControl setAttribute $perfId enabled true

       $AdminControl invoke $perfId reInit

       set enabled [ $AdminControl getAttribute $perfId enabled ]

       puts "New RPA Status is: $enabled\n " 

   } else {

       puts "$serverName is not running. Skip RPA enabling.\n" 

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
# setPerMonOn  
####################################################################

if { [ catch { setPerMonOn $serverName } r ] == 0 } {
    puts "************************************"
    puts "Performance monitoring set successfully" 
    puts "************************************\n"
    puts "\n###### Admin Config Save ######\n"
    $AdminConfig save
} else {
        puts "\nFailed to apply Performance Monitoring settings\n"
        puts $r 
        puts "************************************\n"
}
