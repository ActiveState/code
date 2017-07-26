# 
# Install Application Server.
#
####################################################################
# Patrick Finnegan 26/08/2004.  V1. 
####################################################################

####################################################################
# List installed application servers.
####################################################################
proc showList { a } {

    puts "\nList installed servers"
    puts "\**********************\n"

    foreach e $a {
	regexp {(.*)(\(cells.*)} $e 1 2 3
	puts [ format "%-5s %-50s"  " "  $2 ]
#	puts [ format "%-10s %-50s\n" " "  $3 ]
	lappend returnList                 $2
    }

    return $returnList   
}
####################################################################
# Install Server then create properties for server.
####################################################################
proc installServer { serverName nodeId } {

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

   if { [ catch { setTransProps $serverId $serverName } r ] != 0 } {
	   return -code error $r
   }

#  set Web Container Properties. 

   if { [ catch { setWebProps $serverId $serverName } r ] != 0 } {
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

}
####################################################################
# Set transaction service properties.
####################################################################
proc setTransProps {serverId serverName } {

   global alias 
   global AdminConfig 

   # get Transaction Service id 

   set TransactionServiceId [ $AdminConfig list TransactionService $serverId ]

   set drive [lindex [file split [info script]] 0 ] 

   set clientInactivityTimeout  [ list clientInactivityTimeout  60  ]
   set totalTranLifetimeTimeout [ list totalTranLifetimeTimeout 180 ]
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
proc setWebProps {serverId serverName } {

   global AdminConfig 

   # get Web Container id 

   set WebContainerId [ $AdminConfig list WebContainer $serverId ]

   set defaultVirtualHostName [ list defaultVirtualHostName hbf0035_$serverName ] 
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
   set enableSecurityIntegration     [ list enableSecurityIntegration     true   ]
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
   set invalidationTimeout           [ list invalidationTimeout       30  ] 
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


   set initialHeapSize        [ list initialHeapSize 256 ]
   set maximumHeapSize        [ list maximumHeapSize 256 ]

   # set custom properties.
   ## ws.ext.dirs
  
   set name                   [ list name        ws.ext.dirs                  ]
   set value                  [ list value       {C:\HBFserver_properties  }  ]
   set description            [ list description {Application Property Files} ]

   set wsExtDirs              [ list $name $value $description ]

   ## classloader mode

   set name                   [ list name  {com.ibm.ws.classloader.J2EEApplicationMode} ]
   set value                  [ list value true ]
   set description            [ list description {classloader mode} ]

   set classLoaderMode        [ list $name $value $description ]

   set systemPropertiesList   [ list systemProperties [ list $classLoaderMode $wsExtDirs]]

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
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 1} {
        return -code error "error - no arguments supplied.  Supply server name"
        puts "no arguments"
}

set serverName    [lindex $argv 0]
set nodeName      [ exec hostname ] 
set nodeId        [ $AdminConfig getid /Node:$nodeName/ ]

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

if { [ catch { installServer $serverName $nodeId } r ] == 0 } {
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
