#################################################################### 
# Install App.
####################################################################
# Patrick Finnegan 15/02/2005.  V1. 
####################################################################

######################################
# Proc - check number of arguments
######################################
proc check_args {argc} {
    
    if { $argc < 0 } {

	    error "\nArgument Count is Zero.  No arguments supplied.\n"

	   } else {

            puts "\nargument count = $argc\n"

    }

}
######################################
# Proc - check if dir path exists.  If not create the directory.
######################################
proc check_file { file_name } {
    
    if { [ file exists $file_name ] == 1} {

       puts "File location confirmed for:  $file_name"

       } else {

	   set errMsg "$file_name does not exist.  Create $file_name before running this scipt"
	   return -code error \n$errMsg\n

    }
}
########################################################
# Proc - get user roles from input file and process into list
#      - note that there can be several users to a role so "list user"
########################################################
proc get_userroles {userrolesFileid node cell } {

   puts "executing get_userroles"

   global list_userroleslist

   puts "User roles are ...................."
   puts ""

   while { [ gets $userrolesFileid line ] >=0 } {

       puts "role mapping is: $line"

       lappend roleslist $line 
   }

   set list_userroleslist [list $roleslist]

}
########################################################
# Proc - get group roles from input file and process into list
#      - note that there can be several groups to a role so we map multiple groups
#        to the same role.  This requires an embedded loop.  
########################################################
proc get_grouproles {grouprolesFileid} {

   puts "executing get_grouproles"

   puts "Group roles are ....................\n"

   gets $grouprolesFileid line 

   while { ![ eof $grouprolesFileid ] } {

       set x        [ lindex $line 0 ]
       set appRole  $x 

       while { $appRole == $x && \
               ![ eof $grouprolesFileid ] 
	     } {

	     set ldapRole [ lindex $line 1 ]

	     puts [ format "%-5s %-20s" " " "###########################" ]

	     puts [ format "%-5s %-20s %-20s " " " "Application Role" $appRole  ]
	     puts [ format "%-5s %-20s %-20s " " " "Ldap Role"        $ldapRole ]

	     append groups $ldapRole|

             gets $grouprolesFileid line 

             set x [ lindex $line 0 ]

       }

       lappend groupRoleList [ list $appRole no no ""  $groups] 
       unset groups 

   }

   close  $grouprolesFileid

   return $groupRoleList

}
########################################################
# Proc - get virtual host mappings
#      - note vhosts can be spread across nodes
########################################################
proc get_vhosts {vhostsFileid} {

   puts "\nexecuting get_vhosts\n"

   while { [ gets $vhostsFileid line ] != -1 } {

	   set name   [ lindex $line 0 ]
	   set module [ lindex $line 1 ]
	   set vhost  [ lindex $line 2 ]

	   puts [ format "%-5s %-20s" " " "###########################" ]

	   puts [ format "%-5s %-20s %-20s " " " "Module Name"  $name   ]
	   puts [ format "%-5s %-20s %-20s " " " "Module"       $module ]
	   puts [ format "%-5s %-20s %-20s " " " "Virtual Host" $vhost  ]

	   lappend vhostList [ list $name $module $vhost ] 

       }

   close $vhostsFileid     

   return $vhostList  

} 

   
########################################################
# Proc - get appserver mappings
#      - note webmodules can be spread across appservers
########################################################
proc get_servers {serverFileid cellName nodeName } {

   puts "\nexecuting get_servers\n"

   while { [ gets $serverFileid line ] != -1 } {

	   set name   [ lindex $line 0 ]
	   set module [ lindex $line 1 ]
	   set server [ lindex $line 2 ]

           set serverName WebSphere:cell=$cellName,node=$nodeName,server=$server

	   puts [ format "%-5s %-20s %-20s " " " "Module Name" $name   ]
	   puts [ format "%-5s %-20s %-20s " " " "Module"      $module ]
	   puts [ format "%-5s %-20s %-20s " " " "Server"      $server ]

	   puts [ format "%-5s %-20s" " " "###########################" ]

	   lappend serverList [ list $name $module $serverName ] 

       }

   close $serverFileid     

   return $serverList  

}
########################################################
# Proc - get ejb jndi names
########################################################
proc get_ejbs {ejbFileid} {

   puts "\nexecuting get_ejbs\n"

   while { [ gets $ejbFileid line ] != -1 } {

	   set name   [ lindex $line 0 ]
	   set module [ lindex $line 1 ]
	   set ejb    [ lindex $line 2 ]

	   puts [ format "%-5s %-20s %-20s %-20s" " " $name $module $ejb ]

	   lappend ejbList [ list $name $module $ejb ] 

       }

   close $ejbFileid     

   return $ejbList  
    
}
######################################################
# Proc - install enterprise app.
######################################################
proc installEnterpriseApp { nodeName earFile appName serverName vhostList groupRoleList serverList } {

   global AdminApp

   puts "\ninstallEnterpriseApp\n"

   puts "########################################"
   puts "Creating $appName Enterprise Application"
   puts "########################################"

   set optionList [ list -appname             $appName    \
                         -node                $nodeName   \
		         -server              $serverName \
		         -MapWebModToVH       $vhostList  \
		         -MapRolesToUsers     $groupRoleList \
                         -MapModulesToServers $serverList ]

   if { [ catch { $AdminApp install $earFile $optionList } result_var] == 0 } {

        			       puts $result_var

        			       puts "\n$appName deployed sucessfully\n"

      } else {

              puts \n$result_var\n
              puts "########################################"
              puts "$appName failed to deploy"
              puts "########################################"

	      return -code error $result_var

   }

}

######################################################
# Proc - modify enterprise app.
######################################################
proc modifyEnterpriseApp { appName sessionTimeout } {

   global AdminConfig

   puts "\nmodifyEnterpriseApp"
   puts "_____________________\n"

   puts "########################################"
   puts "Modify $appName Enterprise Application"
   puts "########################################"

   set appId [ $AdminConfig getid /Deployment:$appName ] 

   # get deployed object characteristics.

   set depObject [ $AdminConfig showAttribute $appId deployedObject ] 

   # get current policies.

   set warClassLoader [ $AdminConfig showAttribute $depObject warClassLoaderPolicy ]
   set reloadEnabled  [ $AdminConfig showAttribute $depObject reloadEnabled ]
   set reloadInterval [ $AdminConfig showAttribute $depObject reloadInterval ]

   puts "\n#######################################################"
   puts "Current WAR Class Loader Policy is    $warClassLoader"
   puts "Current WAR Reload Enabled Policy is  $reloadEnabled"
   puts "Current WAR Reload Interval Policy is $reloadInterval"
   puts "#########################################################\n"

   set newWarClassLoaderPolicy  [ list warClassLoaderPolicy SINGLE ] 
   set reloadEnabled            [ list reloadEnabled        true   ]
   set reloadInterval           [ list reloadInterval       3      ]

   set attributes               [ list $newWarClassLoaderPolicy \
                                       $reloadEnabled           \
                                       $reloadInterval          \
                                ]
                                 
   if { [ catch { $AdminConfig modify $depObject $attributes } result_var] == 0 } {

       set warClassLoader [ $AdminConfig showAttribute $depObject warClassLoaderPolicy ]
       set reloadEnabled  [ $AdminConfig showAttribute $depObject reloadEnabled ]
       set reloadInterval [ $AdminConfig showAttribute $depObject reloadInterval ]

       puts "#######################################################"
       puts "New WAR Class Loader Policy is  $warClassLoader"
       puts "New WAR Reload Enabled Policy is  $reloadEnabled"
       puts "New WAR Reload Interval Policy is $reloadInterval"
       puts "#########################################################\n"

   } else {

	      puts \n$result_var\n
	      puts "########################################"
	      puts "$appName - Modification failed"
	      puts "########################################"
              
	      return -code error 

   }

   # set session manager parameters

   set newAllowSerializedSessionAccess [ list allowSerializedSessionAccess false] 
   set newAccessSessionOnTimeOut       [ list accessSessionOnTimeout       true ] 
   set newMaxWaitTime                  [ list maxWaitTime                  90   ] 
   
   # set Tuning Parms 

   set allowOverflow                 [ list allowOverflow           false ]
   set invalidationTimeout           [ list invalidationTimeout     $sessionTimeout ] 
   set maxInMemorySessionCount       [ list maxInMemorySessionCount 1000  ]

   set tuningParamsList [ list $allowOverflow           \
                               $invalidationTimeout     \
                               $maxInMemorySessionCount \
                        ]

   set tuningParams     [ list tuningParams $tuningParamsList ]

   set sessionManagerAttr [ list $newAllowSerializedSessionAccess \
			         $newAccessSessionOnTimeOut       \
				 $newMaxWaitTime                  \
				 $tuningParams                    \
                          ]

   set newSessionManagement  [ list [ list sessionManagement $sessionManagerAttr ] ]

   if { [ catch { $AdminConfig create ApplicationConfig $depObject $newSessionManagement } result_var] == 0 } {

       puts "\nNew Session Manager Attributes for $appName are:\n"
       
       foreach i $sessionManagerAttr {

	   foreach { a b } $i {

	       puts "$a $b"

           }

       }
       
       puts "\n$appName modified sucessfully\n"

       $AdminConfig save

      } else {

	      puts \n$result_var\n
	      puts "########################################"
	      puts "$appName - Modification failed"
	      puts "########################################"
              
	      return -code error 

      }

}
######################################################
# Proc - display attributes.
######################################################
proc displayAttributes { appName } {

   global AdminApp

   puts "displayAttributes"
   puts "_____________________"

   set taskList [ $AdminApp view $appName {-tasknames} ]
  
   foreach x $taskList {

      puts [ format "%-15s %-s " " " "################################" ]
      puts [ format "%-15s %-s " " " "Attributes - $x" ]
      puts [ format "%-15s %-s " " " "################################" ]

      puts [ $AdminApp view $appName -$x ]

   }

}
######################################################
# Proc - nodeSync.
######################################################
proc nodeSync { nodeName } {

   global AdminControl

   puts "\nnodeSync"
   puts "________\n" 

   puts "########################################"
   puts "Sync server application details with node."
   puts "########################################"

   set nodeSync [ $AdminControl queryNames type=NodeSync,node=$nodeName,* ]

   # if the node sync object is null then this is a WAS 5 base instalation.

   if { $nodeSync != {} } {

      puts "\n set enabled flag"
      
      set enabledFlag [ $AdminControl getAttribute $nodeSync serverStartupSyncEnabled ]

      if { [ string compare $enabledFlag false ] == 0 } {

	  puts "\n Syncing node with DM"
	  puts "______________________\n" 

	  if { [ catch { $AdminControl invoke $nodeSync sync } r ] == 0 } {

	      puts "########################################"
	      puts "$nodeName synced sucessfully"
	      puts "########################################"

          }  else { 

	      puts \n$r\n
	      puts "########################################"
	      puts "$nodeName failed to sync"
	      puts "########################################"

          }

      }

   }

}
######################################
# Control block"
######################################

if { [ catch { check_args $argc } r ] != 0 } {

    return -code error $r 

}

set earFile        [ lindex $argv 0 ]
set appName        [ lindex $argv 1 ]
set serverName     [ lindex $argv 2 ]
set userrolesFile  [ lindex $argv 3 ]
set vhostsFile     [ lindex $argv 4 ]
set serverFile     [ lindex $argv 5 ]
set grouprolesFile [ lindex $argv 6 ]
set ejbFile        [ lindex $argv 7 ]
set sessionTimeout [ lindex $argv 8 ]

# Assume one cell, one deployment manager node and one application node. 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodes  [ $AdminConfig list Node ]

# delete the manager node from the list.

set manIndex   [ lsearch -glob $nodes *Manager* ]
set nodeId     [ lindex [ lreplace $nodes $manIndex $manIndex ] 0 ]

# get name attribute for cell and application node

set cellName [ $AdminConfig showAttribute $cellId name ]
set nodeName [ $AdminConfig showAttribute $nodeId name ]


set formatSpec "%-20s %-1s %-1s %s"

puts [ format $formatSpec  "Cell Name"           " " "=" $cellId        ]
puts [ format $formatSpec  "Node Name"           " " "=" $nodeId        ]
puts [ format $formatSpec  "Server Name"         " " "=" $serverName    ]
puts [ format $formatSpec  "Application"         " " "=" $appName       ]
puts [ format $formatSpec  "User Mapping File"   " " "=" $userrolesFile ]
puts [ format $formatSpec  "Ear Mapping File"    " " "=" $earFile ]
puts [ format $formatSpec  "Vhosts Mapping File" " " "=" $vhostsFile ]
puts [ format $formatSpec  "Server Mapping File" " " "=" $serverFile ]
puts [ format $formatSpec  "Group Mapping File"  " " "=" $grouprolesFile ]
puts [ format $formatSpec  "Ejb Mapping File"    " " "=" $ejbFile ]
puts [ format $formatSpec  "Session Timeout"     " " "=" $sessionTimeout ]

puts ""

check_file $earFile        
check_file $userrolesFile  
check_file $grouprolesFile 
check_file $vhostsFile     
check_file $serverFile     
check_file $ejbFile        

puts ""

set userrolesFile_id  [open $userrolesFile   r ]
set grouprolesFile_id [open $grouprolesFile  r ]
set vhostsFileid      [open $vhostsFile      r ]
set serverFileid      [open $serverFile      r ]
set ejbFileid         [open $ejbFile         r ]

if { [ catch { get_vhosts  $vhostsFileid } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

} else {

        set vhostList $r 
	
}

if { [ catch { get_servers $serverFileid $cellName $nodeName } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

} else {

        set serverList $r 
	
}

if { [ catch { get_grouproles $grouprolesFile_id } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

} else {

        set groupRoleList $r 

}

######################################
# Install Application.
######################################

if { [ catch { installEnterpriseApp $nodeName      \
				    $earFile       \
				    $appName       \
				    $serverName    \
				    $vhostList     \
				    $groupRoleList \
				    $serverList } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

} else {

        $AdminConfig save
	
}

######################################
# Modify Application Attributes.
######################################

if { [ catch { modifyEnterpriseApp  $appName $sessionTimeout } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

} else {

        $AdminConfig save
	
}
######################################
# Display Application Attributes.
######################################

if { [ catch { displayAttributes $appName } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

}
######################################
# Sync Node if ND installation.
######################################

if { [ catch { nodeSync $nodeName } r ] != 0 } {

    return -code error \n$r\n 
    exit 1

} 

######################################
# END
######################################
