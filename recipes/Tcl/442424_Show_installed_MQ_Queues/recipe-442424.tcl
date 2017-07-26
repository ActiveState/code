###
### Show installed MQ Queues.
###

proc get_MQQueue {} {

    global AdminConfig
    global AdminControl
    global AdminApp

    set MQQueueIDs [$AdminConfig getid /MQQueue:/]

    set s1 "\nThe currently defined queues are:\n"
    puts   [ format "%-5s %s"  " " $s1 ] 

    foreach MQQueueID $MQQueueIDs {

         set name [ $AdminConfig showAttribute $MQQueueID name ]

         puts [ format "%-20s %s" " " $name ] 

    }

    set s1 "\nThe queue details are:\n"
    
    puts   [ format "%-5s %s"  " " $s1 ] 

    foreach MQQueueID $MQQueueIDs {

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


	 #flatten the list

         set attrsList [ join $attrsList ]

	 array set iArray $attrsList 

	 #sort the indices 

	 set listOfNames [ lsort [ array names iArray ] ]

	 #puts $listOfNames

	 foreach element $listOfNames {

	     puts [ format "%-5s %-20s %s" " " $element $iArray($element) ] 

	 } 


    }

}

get_MQQueue
