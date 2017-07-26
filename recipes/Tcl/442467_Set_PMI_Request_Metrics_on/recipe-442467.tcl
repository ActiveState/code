# 
# Set PMI Request metrics on.
# 
#####################################################################
# Patrick Finnegan 21/10/2005.  V1. 
#####################################################################
#####################################################################
# Get current PMI details. 
####################################################################
proc getPMI { } {

   puts "\n getPMI \n "

   global AdminConfig 

   set PMIRequestMetricsI [ $AdminConfig list PMIRequestMetrics ]

   # get current PMI settings.

   set msg "Current PMI Settings are:\n"

   set enable      [ $AdminConfig showAttribute $PMIRequestMetricsI enable     ]
   set enableARM   [ $AdminConfig showAttribute $PMIRequestMetricsI enableARM  ]
   set traceLevel  [ $AdminConfig showAttribute $PMIRequestMetricsI traceLevel ]
   set filtersList [ split [ $AdminConfig showAttribute $PMIRequestMetricsI filters ] ]
   
   puts [ format "%-5s %s"  " " $msg  ]
       
   puts [ format "%-10s %-20s %-40s"  " " "PMI Enabled:" $enable      ]
   puts [ format "%-10s %-20s %-40s"  " " enableARM      $enableARM   ]
   puts [ format "%-10s %-20s %-40s"  " " traceLevel     $traceLevel  ]

   # filter list is not properly quoted 
   # strip trailing bracket off last element. 
   
   set lastElement [ string trim [ lindex $filtersList end  ] \} ]
   set filtersList [ lreplace $filtersList end end $lastElement ] 

   foreach i $filtersList {

      #puts [ format "\n%-15s %-20s %-40s"  " " "filter is" $i ]

      set type         [ $AdminConfig showAttribute $i type         ]
      set enableF      [ $AdminConfig showAttribute $i enable       ]
      set filterValues [ split [ $AdminConfig showAttribute $i filterValues ] ]

      puts  [ format "\n%-10s %-20s %-40s"  " "  "Filter Type"    $type    ]
      puts  [ format "%-10s %-20s %-40s"    " "  "Filter Setting" $enableF ]

      puts  [ format "%-15s %-20s"    " "  "Filter Details" ] 

      # filterValues list is not properly quoted 
      # strip trailing bracket off last element. 

      set lastElement  [ string trim [ lindex $filterValues end ] \} ]
      
      set filterValues [ lreplace $filterValues end end $lastElement ] 

      foreach i $filterValues {

	 set value   [ $AdminConfig showAttribute $i value  ]
	 set enableV [ $AdminConfig showAttribute $i enable ]

	 puts [ format "%-20s %-10s %-10s" " "    value   $value   ]
	 puts [ format "%-20s %-10s %-10s"   " "  enable  $enableV ] 

      }

   }

}
####################################################################
# Set New PMI Parms. 
# Switch on PMI and add new URIs to URI list.
####################################################################
proc setPMI { uriList } {

   puts "\n setPMI \n "

   global AdminConfig 

   # modify request metrics. 

   set PMIRequestMetricsI [ $AdminConfig list PMIRequestMetrics ]

   set enable      [ list enable     true   ]
   set enableARM   [ list enableARM  false  ]
   set traceLevel  [ list traceLevel HOPS   ]

   set attrs       [ list $enable $enableARM $traceLevel ] 

   puts "\n Modify PMIRequestMetrics with attributes $attrs \n"
   $AdminConfig modify $PMIRequestMetricsI $attrs 

   # modify URI filter

   set filtersList [ split [ $AdminConfig showAttribute $PMIRequestMetricsI filters ] ]
   
   # filter list is not properly quoted 
   # strip trailing bracket off last element. 
   
   set lastElement [ string trim [ lindex $filtersList end  ] \} ]
   set filtersList [ lreplace $filtersList end end $lastElement ] 

   #get uri filter id. 

   foreach filterId $filtersList {

      set type [ $AdminConfig showAttribute $filterId type ]
 
      if { [ string match $type "URI" ] == 1 } {

	  #enable URI filter 

          set enable [ list enable true ]

	  set attrs  [ list $enable     ]

          puts "\n Modify PMIRMFilter URI with $attrs \n"
          $AdminConfig modify $filterId $attrs 

	  #set new filter values

          set filterValues [ split [ $AdminConfig showAttribute $filterId filterValues ] ]

          # filter value list is not properly quoted
          # strip trailing bracket. 

	  set lastElement  [ string trim [ lindex $filterValues end ] \} ]
	  
	  set filterValues [ lreplace $filterValues end end $lastElement ] 

          # check whether any of the new URIs already exist in the filter value list
          # if so delete from the update list.

          foreach i $filterValues {

              set value [ $AdminConfig showAttribute $i value  ]

	      catch { lsearch -glob $uriList $value } r

	      if { $r == -1 } {

		  set continue true 

	      } else {

		  set uriList [ lreplace $uriList $r $r ]

	      }

          }

	  foreach i $uriList {

	     set value  [ list value $i    ]
	     set enable [ list enable true ]

	     set attrList [ list $value $enable ] 

             puts "\n Create PMIRMFilterValue with attributes $attrList \n"
             $AdminConfig create PMIRMFilterValue $filterId $attrList

          }
	      
      }

   }

}
####################################################################
# Main Control.
####################################################################

# Assume one cell, one deployment manager node and one application node. 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodes  [ $AdminConfig list Node ]

# delete the manager node from the list.

set manIndex   [ lsearch -glob $nodes *Manager* ]
set nodeId     [ lindex [ lreplace $nodes $manIndex $manIndex ] 0 ]

# get name attribute for cell and application node

set cellName [ $AdminConfig showAttribute $cellId name ]
set nodeName [ $AdminConfig showAttribute $nodeId name ]

# set URI list.

lappend uriList /contextRoot1 
lappend uriList /contextRoot2 
lappend uriList /contextroot3 
lappend uriList /contextroot4 
lappend uriList /contextroot5 

####################################################################
# setPMIOn  
####################################################################

if { [ catch { getPMI } r ] == 0 } {

     if { [ catch { setPMI $uriList } r ] == 0 } {

	puts "\n************************************"
	puts "Performance monitoring set successfully" 
	puts "************************************\n"

	puts "\n###### Admin Config Save ######\n"
	$AdminConfig save

     } else {

	puts "\n************************************"
        puts "\nFailed to apply Performance Monitoring settings\n"
        puts $r 
        puts "************************************\n"

     }

} else {
	puts "\n************************************"
        puts "\nFailed to apply Performance Monitoring settings\n"
        puts $r 
        puts "************************************\n"
}
