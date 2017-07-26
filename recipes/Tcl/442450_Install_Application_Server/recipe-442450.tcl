# 
# Install Application Server.
#
####################################################################
# Patrick Finnegan 19/10/2005.  V1. 
####################################################################

####################################################################
# List installed application servers.
####################################################################
proc showList { a } {

    puts "\nList installed servers"
    puts "**********************\n"

    foreach e $a {
	regexp {(.*)(\(cells.*)} $e 1 2 3
	puts [ format "%-5s %-50s"  " "  $2 ]
	lappend returnList                 $2
    }

    puts "\n**********************\n"

    return $returnList   
}
####################################################################
# Install Server then create properties for server.
####################################################################
proc installServer { serverName nodeId nonsslPort sslPort rmiPort sessionTimeout tranTimeout } {

   global AdminConfig 

   set nameList [ list name $serverName ]
   set attrList [ list $nameList        ] 

   if { [ catch {$AdminConfig create Server $nodeId $attrList} r ] == 0 } {
        puts "************************************"
        puts "$serverName server created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create $serverName server\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   set serverId [ $AdminConfig getid /Server:$serverName/ ]

   regexp {(.*)(\(cells.*)} $serverId 1 2 3
   set serverName $2

#  set Transaction Service Properties. 

   if { [ catch { setTransProps $serverId $serverName $tranTimeout } r ] != 0 } {
	   return -code error $r
   }

#  set Web Container Properties. 

   if { [ catch { setWebProps $serverId $serverName $nonsslPort $sslPort $sessionTimeout } r ] != 0 } { 
	   return -code error $r
   }

#  set Log File Properties. 

   if { [ catch { setLogProps $serverId $serverName } r ] != 0 } {
	   return -code error $r
   }

#  set JVM Properties. 

   if { [ catch { setJVMProps $serverId $serverName } r ] != 0 } {
	   return -code error $r
   }

#  set Process Definition Properties. 

   if { [ catch { setProcessDefProps $serverId $serverName } r ] != 0 } {
	   return -code error $r
   }

#  set EndPoints Properties. 

   if { [ catch { setEndPointsProps $serverId $serverName $rmiPort } r ] != 0 } {
	   puts "\nfailed - result is $r"
	   return -code error $r
   }
}
####################################################################
# Set transaction service properties.
####################################################################
proc setTransProps { serverId serverName tranTimeout } {

   global alias 
   global AdminConfig 

   # get Transaction Service id 

   set TransactionServiceId [ $AdminConfig list TransactionService $serverId ]

   set drive [lindex [file split [info script]] 0 ] 

   set clientInactivityTimeout  [ list clientInactivityTimeout  60  ]
   set totalTranLifetimeTimeout [ list totalTranLifetimeTimeout $tranTimeout ]
   set transactionLogDirectory  [ list transactionLogDirectory  " " ]

   set attrList  [ list $clientInactivityTimeout  \
                        $totalTranLifetimeTimeout \
                        $transactionLogDirectory  \
                 ]

   if { [ catch { $AdminConfig modify $TransactionServiceId $attrList } r ] == 0 } {
        puts "************************************"
        puts "$serverName transaction properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create transaction properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }
}
####################################################################
# Set web container properties.
####################################################################
proc setWebProps {serverId serverName nonsslPort sslPort sessionTimeout } {

   global AdminConfig 

   # get Web Container id 

   set WebContainerId [ $AdminConfig list WebContainer $serverId ]

   set defaultVirtualHostName [ list defaultVirtualHostName intg_$serverName ] 
   set enableServletCaching   [ list enableServletCaching   true ] 

   set attrList [ list $defaultVirtualHostName \
                       $enableServletCaching   \
                ]

   if { [ catch { $AdminConfig modify $WebContainerId $attrList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - WebContainer properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create WebContainer properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   # get ThreadPool id 

   set threadPoolId [ lindex [ $AdminConfig list ThreadPool $WebContainerId ] 0 ]

   set inactivityTimeout  [ list inactivityTimeout 3500  ]
   set isGrowable         [ list isGrowable        true  ]
   set maximumSize        [ list maximumSize       50 ]
   set minimumSize        [ list minimumSize       10 ]

   set threadPoolList  [ list $inactivityTimeout   \
                              $isGrowable          \
                              $maximumSize         \
                              $minimumSize         \
                       ]

   if { [ catch { $AdminConfig modify $threadPoolId $threadPoolList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - Threadpool properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Threadpool properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   # get Session Manager id 

   set sessionManagerId [ $AdminConfig list SessionManager $WebContainerId]

   set accessSessionOnTimeout        [ list accessSessionOnTimeout        true   ]
   set allowSerializedSessionAccess  [ list allowSerializedSessionAccess  false  ] 
   set enable                        [ list enable                        true   ]
   set enableCookies                 [ list enableCookies                 true   ]
   set enableProtocolSwitchRewriting [ list enableProtocolSwitchRewriting false  ]
   set enableSSLTracking             [ list enableSSLTracking             false  ]
   set enableSecurityIntegration     [ list enableSecurityIntegration     false  ]
   set enableUrlRewriting            [ list enableUrlRewriting            false  ]
   set maxWaitTime                   [ list maxWaitTime                   5      ]

   set sessionManagerList [ list $accessSessionOnTimeout        \
                                 $allowSerializedSessionAccess  \
                                 $enable                        \
                                 $enableCookies                 \
                                 $enableProtocolSwitchRewriting \
                                 $enableSSLTracking             \
                                 $enableSecurityIntegration     \
                                 $enableUrlRewriting            \
                                 $maxWaitTime                   \
                          ]

   if { [ catch { $AdminConfig modify $sessionManagerId $sessionManagerList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - Session Manager properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Session Manager properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   # get Tuning Parms 

   set tuningParamsId [ $AdminConfig list TuningParams $WebContainerId ]

   set allowOverflow                 [ list allowOverflow           false ]
   set invalidationTimeout           [ list invalidationTimeout     $sessionTimeout ] 
   set maxInMemorySessionCount       [ list maxInMemorySessionCount 1000  ]

   set tuningParamsList [ list $allowOverflow           \
                               $invalidationTimeout     \
                               $maxInMemorySessionCount \
                       ]

   if { [ catch { $AdminConfig modify $tuningParamsId $tuningParamsList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - Tuning properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Tuning properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   # get http transports id. 

   set httpTransportIdList [ $AdminConfig list HTTPTransport $WebContainerId ]

   # assume two default host entries.  
   # modify host entries with new values.

   # Transport 1.
   set transport1     [ lindex $httpTransportIdList 0 ]
   set addressId [ $AdminConfig showAttribute $transport1 address ] 
   set oldHost   [ $AdminConfig showAttribute $addressId host ]
   set oldPort   [ $AdminConfig showAttribute $addressId port ]

   puts "Old Host is $oldHost " 
   puts "Old Port is $oldPort " 

   set newHost     [ list host *           ]
   set newPort     [ list port $nonsslPort ]
   set addressList [ list $newHost $newPort  ]

   puts "New Host is $oldHost" 
   puts "New Port is $newPort" 

   if { [ catch { $AdminConfig modify $addressId $addressList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - HTTP Transport properties modified successfully."
        puts "************************************\n"
   } else {
           puts "************************************"
           puts "\nfailed to create modify HTTP Transport properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   # Transport2.
   set transport2 [ lindex $httpTransportIdList 1 ]
   set addressId  [ $AdminConfig showAttribute $transport2 address ] 
   set oldHost    [ $AdminConfig showAttribute $addressId host ]
   set oldPort    [ $AdminConfig showAttribute $addressId port ]

   puts "Old Host is $oldHost " 
   puts "Old Port is $oldPort " 

   set newHost     [ list host *            ]
   set newPort     [ list port $sslPort     ]
   set addressList [ list $newHost $newPort ]

   puts "New Host is $oldHost" 
   puts "New Port is $newPort" 

   if { [ catch { $AdminConfig modify $addressId $addressList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - HTTP Transport properties modified successfully."
        puts "************************************\n"
   } else {
           puts "************************************"
           puts "\nfailed to create modify HTTP Transport properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }
   
}
####################################################################
# Set logging properties.
####################################################################
proc setLogProps {serverId serverName } {

   global AdminConfig 

   # get websphere install directory from node variable map. 

   set nodeVarMapId [ $AdminConfig getid /Node:[exec hostname]/VariableMap:/ ]
   set listVar1     [ eval join  [ $AdminConfig showall $nodeVarMapId ] ]
   set x            [ lindex [ lindex $listVar1 [lsearch $listVar1 *WAS_INSTALL_ROOT*] ] 2 ]
   set WAS_INSTALL_ROOT [ lindex [ split $x ] 1 ]

   # get output log id 

   set outputLogId [ $AdminConfig showAttribute $serverId outputStreamRedirect ]

   set baseHour               [ list baseHour 24 ]
   set fileName               [ list fileName $WAS_INSTALL_ROOT\\logs\\$serverName\\$serverName\_SystemOut.log ]
   set formatWrites           [ list formatWrites           true   ]
   set maxNumberOfBackupFiles [ list maxNumberOfBackupFiles 5      ]
   set messageFormatKind      [ list messageFormatKind      BASIC  ]
   set rolloverPeriod         [ list rolloverPeriod         24     ]
   set rolloverSize           [ list rolloverSize           5      ]
   set rolloverType           [ list rolloverType           TIME   ]
   set suppressStackTrace     [ list suppressStackTrace     false  ]
   set suppressWrites         [ list suppressWrites         false  ]

   set attrList [ list $baseHour               \
                       $fileName               \
                       $formatWrites           \
                       $maxNumberOfBackupFiles \
                       $messageFormatKind      \
                       $rolloverPeriod         \
                       $rolloverSize           \
                       $rolloverType           \
                       $suppressStackTrace     \
                       $suppressWrites         \
                ]
   
   if { [ catch { $AdminConfig modify $outputLogId $attrList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - Server output log properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Server output log properties for $serverName\n"
           puts $r 
           puts "************************************\n"
	   return -code error $r
   }

   # get error log id 

   set errorLogId [ $AdminConfig showAttribute $serverId errorStreamRedirect ]

   set baseHour               [ list baseHour 24 ]
   set fileName               [ list fileName $WAS_INSTALL_ROOT\\logs\\$serverName\\$serverName\_SystemErr.log ]
   set formatWrites           [ list formatWrites           true   ]
   set maxNumberOfBackupFiles [ list maxNumberOfBackupFiles 5      ]
   set messageFormatKind      [ list messageFormatKind      BASIC  ]
   set rolloverPeriod         [ list rolloverPeriod         24     ]
   set rolloverSize           [ list rolloverSize           5      ]
   set rolloverType           [ list rolloverType           TIME   ]
   set suppressStackTrace     [ list suppressStackTrace     false  ]
   set suppressWrites         [ list suppressWrites         false  ]

   set attrList [ list $baseHour               \
                       $fileName               \
                       $formatWrites           \
                       $maxNumberOfBackupFiles \
                       $messageFormatKind      \
                       $rolloverPeriod         \
                       $rolloverSize           \
                       $rolloverType           \
                       $suppressStackTrace     \
                       $suppressWrites         \
                ]

   if { [ catch { $AdminConfig modify $errorLogId $attrList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - Server error log properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Server error log properties for $serverName\n"
           puts $r 
           puts "************************************\n"
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


   set initialHeapSize        [ list initialHeapSize 128 ]
   set maximumHeapSize        [ list maximumHeapSize 256 ]

   # set custom properties.
   ## ws.ext.dirs
  
   set name                   [ list name        ws.ext.dirs                  ]
   set value                  [ list value       {d:\HBFWeb\properties}  ]
   set description            [ list description {Application Property Files} ]

   set wsExtDirs              [ list $name $value $description ]

   set systemPropertiesList   [ list systemProperties [ list $wsExtDirs]]

   set attrList [ list $initialHeapSize        \
                       $maximumHeapSize        \
                       $systemPropertiesList   \
                ]

   if { [ catch { $AdminConfig modify $jvmId $attrList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - JVM properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Server JVM properties for $serverName\n"
           puts "************************************\n"
	   return -code error $r
   }

}
####################################################################
# Set Process Definition Properties.
####################################################################
proc setProcessDefProps {serverId serverName } {

   global AdminConfig 

   set processDefId [ $AdminConfig showAttribute $serverId processDefinition ]

   set monPolicyId  [$AdminConfig showAttribute $processDefId monitoringPolicy ]

   set monPolicy    [ list nodeRestartState PREVIOUS ] 

   set attrList     [ list $monPolicy ]

   if { [ catch { $AdminConfig modify $monPolicyId $attrList } r ] == 0 } {
        puts "************************************"
        puts "$serverName - Process Definition properties created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create Process Definition properties for $serverName\n"
           puts "************************************\n"
	   return -code error $r
   }

}
####################################################################
# Set Endpoints - RMI. 
####################################################################
proc setEndPointsProps {serverId serverName rmiPort } {

   global AdminConfig 

   set endPointsId      [ $AdminConfig getid /ServerEntry:$serverName/ ]

   set specialEndPoints [ $AdminConfig showAttribute $endPointsId specialEndpoints ]

   # specialEndPoints is a one element list containing an embedded list. 
  
   set listlength [ llength [ lindex $specialEndPoints 0 ] ]

   set listElements [ expr { $listlength - 1 } ] 

   # iterate through the sublist and find the bootstrap address.

   set i 0

   while { $i <= $listElements } {

       set endPoint [ lindex [ lindex $specialEndPoints 0 ] $i ]

       set endPointName [ $AdminConfig showAttribute $endPoint endPointName ] 

       if { $endPointName == "BOOTSTRAP_ADDRESS" } {

          set endPointId [ $AdminConfig showAttribute $endPoint endPoint ] 
          set port       [ $AdminConfig showAttribute $endPointId port ]

	  puts "End Point Name = $endPointName"
	  puts "Old port       = $port"

	  set newPort  [ list port $rmiPort ] 
	  set attrList [ list $newPort ] 

	  if { [ catch { $AdminConfig modify $endPointId $attrList } r ] == 0 } {

	       puts "************************************"
	       puts "End Point Name = $endPointName"
	       puts "New port       = $rmiPort"
	       puts "$serverName - End Points modified successfully."
	       puts "************************************\n"

	  } else {
	          puts "************************************"
	          puts "\nfailed to modify End Points for $serverName\n"
	          puts "************************************\n"
	          return -code error $r
	  }

       }

       incr i

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
set nonsslPort     [ lindex $argv 1 ]
set sslPort        [ lindex $argv 2 ]
set rmiPort        [ lindex $argv 3 ]
set sessionTimeout [ lindex $argv 4 ]
set tranTimeout    [ lindex $argv 5 ]

puts "server name    = $serverName"
puts "nonsslPort     = $nonsslPort"  
puts "sslPort        = $sslPort"  
puts "rmiPort        = $rmiPort"   
puts "sessionTimeout = $sessionTimeout"   
puts "tranTimeout    = $tranTimeout"   

#######################################################################
# List servers and check if target server already exists.
# If so delete it and recreate
#######################################################################

set servers [ $AdminConfig list Server ]

catch { showList $servers } r

catch {lsearch $r $serverName } r 

if { $r == -1 } {
    set continue true 
} else { 
        set serverId [ $AdminConfig getid /Server:$serverName/ ]
        catch { $AdminConfig remove $serverId } r
	puts $r
}
####################################################################
# Install Server 
####################################################################

if { [ catch { installServer $serverName $nodeId $nonsslPort $sslPort $rmiPort $sessionTimeout $tranTimeout } r ] == 0 } {
    puts "************************************"
    puts "$serverName installed successfully"
    puts "************************************\n"
    puts "\n###### Admin Config Save ######\n"
    $AdminConfig save
} else {
        puts "\n$serverName failed to install\n"
        puts $r 
        puts "************************************\n"
}

####################################################################
# List servers to verify install 
####################################################################

set servers [ $AdminConfig list Server ]

catch { showList $servers } r
