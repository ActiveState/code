###   
### set_MQ_Queues.jacl   
###   
###   
###   
###   
###   
   
proc set_MQQueue {MQJMSProviderID nname mqqmgr queueList} {   
   
   
###   
### set up globals   
###   
   
global AdminConfig   
global AdminControl   
global AdminApp   
   
foreach {qName bqName} $queueList {
    
    puts "Creating $qName $bqName ..."
    
    set CCSID			[ list CCSID 1208		]
    set baseQueueManagerName	[ list baseQueueManagerName $mqqmgr ]
    set baseQueueName		[ list baseQueueName $bqName	]
    set decimalEncoding		[ list decimalEncoding Normal	]
    set description		[ list description $qName	]
    set expiry			[ list expiry APPLICATION_DEFINED ]
    set floatingPointEncoding 	[ list floatingPointEncoding IEEENormal ]
    set integerEncoding		[ list integerEncoding Normal	]
    set jndiName	    	[ list jndiName mq/$qName	]
    set name			[ list name $qName		]
    set persistence		[ list persistence APPLICATION_DEFINED ]
    set priority		[ list priority APPLICATION_DEFINED ]
    set targetClient		[ list targetClient MQ		]
    set useNativeEncoding	[ list useNativeEncoding true	]
    	
    set attrs [ list $CCSID        	  \
                    $baseQueueManagerName \
                    $baseQueueName        \
                    $decimalEncoding      \
		    $description          \
                    $expiry               \
		    $floatingPointEncoding \
	       	    $integerEncoding	  \
    		    $jndiName		  \
    		    $name	          \
    		    $persistence	  \
    		    $priority		  \
    		    $targetClient	  \
		    $useNativeEncoding   			    
	     ]

   ##puts " ATTRS = $attrs"

   if { [ catch { $AdminConfig create MQQueue $MQJMSProviderID $attrs } r ] == 0 } {

       $AdminConfig save
       
       } else {

       puts "\nproblem creating MQQueue $qName. \n"
       puts $r 
       puts "************************************\n"
       return -code error $r
   }
    
}

### Synchronize nodes
puts "Synchronizing nodes..."

set Sync1 [$AdminControl completeObjectName type=NodeSync,node=$nname,*]

set xstatus [$AdminControl invoke $Sync1 sync]
puts $xstatus

if {$xstatus == "false"} {
    puts "Unable to synchronize..."
}
   
}   
   
###   
### Main   
###   
if { !($argc == 15) } {   
   puts ""   
   puts "Insufficient arguments supplied on command line:  "   
   puts " "   
} else {    
   set MQJMSProviderID    [lindex $argv 0]
   set nname              [lindex $argv 1]	
   set mqqmgr             [lindex $argv 2]
   set qname1             [lindex $argv 3]
   set mqqueue1  	  [lindex $argv 4]
   set qname2             [lindex $argv 5]
   set mqqueue2  	  [lindex $argv 6]
   set qname3             [lindex $argv 7]
   set mqqueue3  	  [lindex $argv 8]
   set qname4             [lindex $argv 9]
   set mqqueue4  	  [lindex $argv 10]
   set qname5             [lindex $argv 11]
   set mqqueue5  	  [lindex $argv 12]
   set qname6             [lindex $argv 13]
   set mqqueue6  	  [lindex $argv 14]
   set queueList	  [list $qname1 $mqqueue1 $qname2 $mqqueue2 $qname3 $mqqueue3 $qname4 $mqqueue4 $qname5 $mqqueue5 $qname6 $mqqueue6 ]
   set_MQQueue $MQJMSProviderID $nname $mqqmgr $queueList
}
