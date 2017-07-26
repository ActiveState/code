####################################################################
# take a java core dump from a running server. ####################################################################
proc dumpThreads { serverName } {

   global AdminConfig
   global AdminControl

   putsLog "[ lindex [ info proc ] 0 ]" 

   foreach i [ info args dumpThreads ]  {

      upvar 0 $i ilocal

      set propertiesArray($i) $ilocal 

   }

   putsLog "properties are.................."

   foreach { a b } [ array get propertiesArray ] {

       putsLog [ format "%-25s %s" "$a" "$b" ]

   }

   set serverId [ $AdminConfig getid /Server:$serverName ]
   #set serverId  [$AdminControl completeObjectName type=JVM,process=$serverName,*]

   if { [ string length $serverId ] == 0 } {

      putsLog "ERROR: $serverName does not exist" 

      return -code error 

   }

   # get the location of the working directory from the process definition child of the server object.

   #set processDefinitionId [ lindex [ $AdminConfig showAttribute $serverId processDefinitions ] 0 ]
   set processDefinitionId [ lindex [ $AdminConfig showAttribute $serverId processDefinition ] 0 ]

   set workingDirectory [ $AdminConfig showAttribute $processDefinitionId workingDirectory ]
   
   # if the working directory value is a variable rather than a physical directory get the value of the variable from the node variable map. 

   if { [ file isfile $workingDirectory ] == 1 } {

          # get the node name by parsing the server object id string
          putsLog "find the variable"

	  set x [ expr [ string first "nodes/" $serverId ] + 6 ] 

	  set y [ expr { [ string first "/" $serverId $x ] -1 } ] 

	  set nodeName [ string range $serverId $x $y ]

	  set nodeVarMapId [ $AdminConfig getid /Node:$nodeName/VariableMap:/ ]

          set entriesId [ $AdminConfig showAttribute $nodeVarMapId entries ]
 
          # sort and print the variables 

	  foreach i [ lindex $entriesId 0 ] { 
	      
	      lappend varList [ list [ $AdminConfig showAttribute $i symbolicName ] [ $AdminConfig showAttribute $i value ] $i ] 
	  
          } 

          set varList [ lsort -index 0 $varList  ]

	  putsLog "variable list is......................."

	  foreach e $varList { putsLog [ format "%-30s %-s" "[ lindex $e 0 ]" "[ lindex $e 1 ]" ] }  

          # strip the $ and braces off the variable.

          set workDirVar [ string trimright [string trimleft "\$\{USER_INSTALL_ROOT\}" "\$\{"] "\}" ]          

          # look for a match.

	  foreach i $varList { 
	     
	      if { [ string match $workDirVar [ lindex [ lindex $i 0 ] 0 ] ] == 1 } {
	          
	          putsLog "match............."
	          putsLog "working directory is [ lindex [ lindex $i 0 ] 0 ] [ lindex [ lindex $i 1 ] 0 ]"

                  break 

              }
          }

   } else {

        putsLog "working directory is $workingDirectory"

   }        

   # dump the threads
   # The server must be running.  Get the mbean.

   if { [ catch { $AdminControl completeObjectName type=JVM,process=$serverName,* } r ] == 0 } {

       if { [ string length $r ] == {} } {

	  putsLog " $serverName not running" 

	  return -code error 

       } else {

	   set jvmId $r

           putsLog "dumping threads....................."

	   if { [ catch { $AdminControl invoke $jvmId dumpThreads } r ] == 0 } {

	        putsLog "$serverName - threads dumped successfully"
	 
	   } else {

	       return -code error $r

           }
       }

   } else {

               putsLog $r
	       return -code error $r

   }

           putsLog "*** the End ***"
}
