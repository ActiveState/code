###   
### installMQQCF.tcl
###   
### Installs Websphere MQ Queue Connection Factory at the Node level - name WebSphereQCF
###   
   
proc set_MQ_QCF {MQJMSProviderID nname qcfname mqhname mqchannel mqport mqqmgr} {   
   
   
###   
### set up globals   
###   
   
global AdminConfig   
global AdminControl   
global AdminApp   

###
### create Websphere MQ Queue Connection Factory
###

set XAEnabled          [ list XAEnabled true         ]
set channel            [ list channel $mqchannel     ]
set agedTimeout        [ list agedTimeout 0          ]      
set connectionTimeout  [ list connectionTimeout 180  ]
set maxConnections     [ list maxConnections 50      ]
set minConnections     [ list minConnections 1       ]
set purgePolicy        [ list purgePolicy FailingConnectionOnly ]
set reapTime	       [ list reapTime 180           ]
set unusedTimeout      [ list unusedTimeout 1800     ]
set connectionPool     [ list connectionPool [list $agedTimeout $connectionTimeout $maxConnections $minConnections $purgePolicy $reapTime $unusedTimeout ] ]
set description        [ list description "$qcfname" ]
set host               [ list host $mqhname          ]
set jndiName           [ list jndiName mq/$qcfname   ]
set authDataAlias      [ list authDataAlias none     ]
set mappingConfigAlias [ list mappingConfigAlias DefaultPrincipalMapping ]
set mapping            [ list mapping [list $authDataAlias $mappingConfigAlias ] ]
set msgRetention       [ list msgRetention true      ]
set name	       [ list name "$qcfname"        ]
set port	       [ list port $mqport	     ]
set queueManager       [ list queueManager $mqqmgr   ]
set agedTimeout1       [ list agedTimeout 0          ]      
set connectionTimeout1 [ list connectionTimeout 180  ]
set maxConnections1    [ list maxConnections 10      ]
set minConnections1    [ list minConnections 1       ]
set purgePolicy1       [ list purgePolicy FailingConnectionOnly ]
set reapTime1          [ list reapTime 180           ]
set unusedTimeout1     [ list unusedTimeout 1800     ]
set sessionPool        [ list sessionPool [ list $agedTimeout1 $connectionTimeout1 $maxConnections1 $minConnections1 $purgePolicy1 $reapTime1 $unusedTimeout1 ] ]
set CCSID	       [ list CCSID 819              ]
set transportType      [ list transportType CLIENT   ]

   set attrs [ list $XAEnabled        	\
                    $channel		\
                    $connectionPool    	\
                    $description      	\
                    $host               \
		    $jndiName           \
                    $mapping            \
		    $msgRetention       \
	       	    $name	        \
    		    $port		\
    		    $queueManager	\
    		    $sessionPool	\
    		    $CCSID		\
    		    $transportType				    
	     ]

   puts " ATTRS = $attrs"

   if { [ catch { $AdminConfig create MQQueueConnectionFactory $MQJMSProviderID $attrs } r ] == 0 } {

       $AdminConfig save
       
       } else {

       puts "\nproblem creating MQQueueConnectionFactory $MQJMSProviderID. \n"
       puts $r 
       puts "************************************\n"
       return -code error $r
   }

### Synchronize nodes

puts "Synchronizing nodes..."
set Sync1 [$AdminControl completeObjectName type=NodeSync,node=$nname,*]
set xstatus [$AdminControl invoke $Sync1 sync]

if {$xstatus == "false"} {
    puts "Unable to synchronize nodes..."
}
   
}   
      
###   
### Main   
###   
if { !($argc == 7) } {   
   puts ""   
   puts "Insufficient arguments supplied on command line:  "   
   puts " "   
} else {    
   set MQJMSProviderID    [lindex $argv 0]
   set nname              [lindex $argv 1]	
   set qcfname            [lindex $argv 2]
   set mqhname            [lindex $argv 3]
   set mqchannel	  [lindex $argv 4]
   set mqport             [lindex $argv 5]
   set mqqmgr             [lindex $argv 6]
   set_MQ_QCF $MQJMSProviderID $nname $qcfname $mqhname $mqchannel $mqport $mqqmgr 
}   
