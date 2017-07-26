###
### Show installed MQ connection factories. 
###

proc getMQQueueFactories {} {

    global AdminConfig

    set s1 "\nThe currently defined factories are:\n"

    puts   [ format "%-5s %s"  " " $s1 ] 

    set MQQueueConnectionFactories [ $AdminConfig getid /MQQueueConnectionFactory:/ ]

    foreach MQQueueID $MQQueueConnectionFactories {

         set name [ $AdminConfig showAttribute $MQQueueID name ]

         puts [ format "%-20s %s" " " $name ] 

    }

    set s1 "\nThe queue connection factory details are:\n"
    
    puts   [ format "%-5s %s"  " " $s1 ] 

    foreach MQQueueID $MQQueueConnectionFactories {

         set name [ $AdminConfig showAttribute $MQQueueID name ]

         puts [ format "\n%-20s %s" " " $name ] 

	 set i 0

	 while { $i <= [ string length $name ] } {

	     append underLine * 

	     incr i

         }

         puts [ format "%-20s %s\n" " " $underLine ] 

	 unset underLine

         set attrsList [ $AdminConfig showall $MQQueueID ]

         puts $attrsList

    }

}

getMQQueueFactories
