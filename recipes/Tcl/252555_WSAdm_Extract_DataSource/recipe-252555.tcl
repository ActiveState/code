# 
# Extract DataSource Properties 
#


####################################################################
# List installed DataSources. 
####################################################################
proc showList { a } {

    foreach e $a {
	regexp {(.*)(\(cells.*)} $e 1 2 3
	puts [ format "%-5s %-50s\n"  " "  $2 ]
	puts [ format "%-10s %-50s\n" " "  $3 ]
	lappend returnList                 $2
    }

    return $returnList   
}
####################################################################
# List JAAS authentication entries. 
####################################################################
proc listJAAS { a } {

   global AdminConfig 

   foreach e $a {

      set subList [ $AdminConfig show $e ]

      foreach e $subList {
         puts [ format "%-5s %-30s %-20s" " " [ lindex $e 0 ] [ lindex $e 1 ] ]
      }

      puts "\n" 
   }

}

####################################################################
# Show properties of Installed DataSources.
####################################################################
proc showProperties {dataSourceId} {

   set dataSource [ string range $dataSourceId 0 [ expr [string first "(cells" $dataSourceId] -1 ] ]

   puts "\n *** - showProperties - dataSource is $dataSource - *** \n" 

   global AdminConfig 

   puts [ format "\n%-5s %-30s" " " "Display General Properties\n"]

   lappend propList authDataAlias 
   lappend propList authMechanismPreference 
   lappend propList description
   lappend propList name
   lappend propList jndiName
   lappend propList provider
   lappend propList relationalResourceAdapter
   lappend propList statementCacheSize
   lappend propList datasourceHelperClassname

   foreach e $propList {
        set attrValue [ $AdminConfig showAttribute $dataSourceId $e ]

	if { $e == "provider" || $e == "relationalResourceAdapter" } {
	    regexp {(.*)(\(cells.*)} $attrValue 1 2 3
	    set attrValue $2
        }
	puts [ format "%-5s %-30s %-20s" " " $e $attrValue ]
   }

#  Extract mapping properties from mapping list 
#  may not exist for all datasource types.
#  wsadmin returns variables even when they do not exist so cannot use info exist.

   puts [ format "\n%-5s %-30s" " " "Display mapping properties\n"]
   
   set mappingId [$AdminConfig show $dataSourceId mapping]

   if {[string length $mappingId] != 0 } {

       set mappingId [lindex [split [$AdminConfig show $dataSourceId mapping]] 1]

       regsub -all "\}" $mappingId "" mappingId
       
       foreach e [$AdminConfig showall $mappingId] {
	  puts [ format "%-5s %-30s %-20s" " " [lindex $e 0] [lindex $e 1] ]
       }
   }

#  Extract propertySet properties from propertySet list 

   set propertySetId [lindex [split [$AdminConfig show $dataSourceId propertySet]] 1]

   puts [ format "\n%-5s %-30s" " " "Display Custom Properties\n"]

   regsub -all "\}" $propertySetId "" propertySetId
   
   set propertySetList [ $AdminConfig showall $propertySetId ] 

   set i 0
   
   while { $i <= 7 } {

      set sublist [ lindex [ lindex [ lindex $propertySetList 0 ] 1 ] $i ]

      foreach e $sublist {
 
	 if {[lindex $e 0] == "description"} {
	     set continue true
         } else {
                 puts [ format "%-5s %-30s %-20s" " " [ lindex $e 0]  [ lindex $e 1 ] ]
         }
      }

      incr i
      puts \n 
   }
	
#  Extract connectionPool properties from connectionPool list 

   puts [ format "\n%-5s %-30s" " " "Display Connection Pool properties\n"]

   set connectionPoolId [lindex [split [$AdminConfig show $dataSourceId connectionPool]] 1]
   regsub -all "\}" $connectionPoolId "" connectionPoolId
   
   foreach e [$AdminConfig showall $connectionPoolId] {
      puts [ format "%-5s %-30s %-20s" " " [lindex $e 0] [lindex $e 1] ]
   }

}
####################################################################
# Main Control.
####################################################################

####################################################################
# List Installed DataSources.
####################################################################
set datasources [ $AdminConfig list DataSource ]

puts "\nList installed DataSources\n"

catch { showList $datasources } r

####################################################################
# List JAASAuthData authentication entries.
####################################################################

set JAASentries [ $AdminConfig list JAASAuthData ] 

puts "\nList installed JAASAuthData authentication entries\n"

listJAAS $JAASentries

####################################################################
# Show properties for each datasource.
####################################################################

foreach e $datasources {

   showProperties $e 

}

####################################################################
# The end.
####################################################################

puts [ format "\n %-30s %-30s" " " "*** THE END ***\n" ]
