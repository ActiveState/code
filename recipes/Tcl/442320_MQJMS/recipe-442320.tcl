###########################################################
# Connect to MQ listener and put message on the queue.
###########################################################

puts "\n executing [info script]\n"

# make script drive independent.

set drive [lindex [file split [info nameofexecutable]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

########################################################  
# Source packages. 
########################################################  

package require java

######################################
# Proc - check mq listener. 
######################################
proc checkMQ { QManager CCSID channel hostname queueName port traceFile msg } {

   puts "\n checkMQ \n"

   # import required classes 
   java::import com.ibm.mq.jms.MQQueueConnectionFactory
   java::import com.ibm.mq.jms.services.ConfigEnvironment
   java::import com.ibm.mq.jms.JMSC
   java::import com.ibm.mq.jms.MQQueueSession
   java::import com.ibm.mq.jms.MQQueueSender

   # instanciate MQQueueConnectionFactoryI object.
   set MQQueueConnectionFactoryI [ java::new MQQueueConnectionFactory ]

   # set MQQueueConnectionFactory instance methods.
   $MQQueueConnectionFactoryI setQueueManager         $QManager
   $MQQueueConnectionFactoryI setPort                 $port
   $MQQueueConnectionFactoryI setHostName             $hostname
   $MQQueueConnectionFactoryI setChannel              $channel
   $MQQueueConnectionFactoryI setCCSID                $CCSID
   $MQQueueConnectionFactoryI setUseConnectionPooling true
   $MQQueueConnectionFactoryI setTransportType        [ java::field JMSC MQJMS_TP_CLIENT_MQ_TCPIP ]    

   # set tracing on.
   java::call ConfigEnvironment start
   
   puts "Creating a Connection...................\n"

   set connectionI [ $MQQueueConnectionFactoryI createQueueConnection ]

   puts "Starting the Connection.................\n"

   $connectionI start

   puts "Creating a Session......................\n"

   set transacted      false 
   set autoAcknowledge [ java::field MQQueueSession AUTO_ACKNOWLEDGE ]
   set sessionI        [ $connectionI createQueueSession $transacted $autoAcknowledge ]

   puts "Creating a queue......................\n"

   set queueI         [ $sessionI createQueue $queueName ]

   puts "Creating a queue sender ......................\n"

   set queueSenderI  [ $sessionI createSender $queueI ] 

   puts "Sending the message to..[ $queueI getQueueName ]\n" 

   puts "Creating a TextMessage........................\n"

   set outMsgI [ $sessionI createTextMessage ]

   $outMsgI    setText $msg

   puts "Sending TextMessage \"$msg\" \n"

   $queueSenderI send $outMsgI
   
   puts "Closing QueueSender........................\n"

   $queueSenderI close 

   puts "Closing Session............................\n"

   $sessionI close 

   puts "Closing Connection.........................\n"

   $connectionI close 

}
######################################
# Main Control.
######################################

# build tcl classpath

append x $drive/IBM/WebSphereMQ/Java/lib/com.ibm.mq.jar\;
append x $drive/IBM/WebSphereMQ/Tools/Java/base\;
append x $drive/IBM/WebSphereMQ/Java/lib/com.ibm.mqjms.jar\;
append x $drive/IBM/WebSphereMQ/Tools/Java/jms\;
append x $drive/IBM/WebSphereMQ/Java/lib/com.ibm.mqbind.jar\;

set env(TCL_CLASSPATH) $x

puts "\nTCL_CLASSPATH = [ array get env TCL_CLASSPATH ]\n"

set traceFile    $drive/IBM/WebSphereMQ/Errors/mqTrace.txt
set reportFile   $drive/reports/notify/mqConnect.txt
set reportFileId [ open $reportFile w ] 

set QManager  YourQueueManager
set CCSID     819
set channel   your.channel.definition
set hostname  mqHost
set queueName your.queue.name
set port      1414
set msg       "Watson, please come here. I want you."

checkMQ $QManager $CCSID $channel $hostname $queueName $port $traceFile $msg 
