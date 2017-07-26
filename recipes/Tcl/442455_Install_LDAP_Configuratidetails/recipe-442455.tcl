# 
# Install LDAP Settings.
#
####################################################################
# Patrick Finnegan 19/09/2005.  V1. 
####################################################################

#-------------------------------------------------------------------------------
# Get List LDAP Registries. 
#-------------------------------------------------------------------------------

proc getLDAPUserRegistryId {} {

   global AdminConfig 

   puts "\n## List Registry Details ##\n" 

   # Note: IBM advise that there can only be one ldap server per cell.

   if { [ catch { $AdminConfig list LDAPUserRegistry } r ] == 0 } {

       set LDAPUserRegistryId $r

       foreach e $r {

          puts [ format "\n%-10s %-50s\n"  "Registry:" $e  ]

          catch { $AdminConfig showAttribute $e baseDN           } r
	  puts [ format "%-5s %-20s %-50s"  " " baseDN $r ]
          catch { $AdminConfig showAttribute $e bindDN           } r
	  puts [ format "%-5s %-20s %-50s"  " " bindDN $r ]
          catch { $AdminConfig showAttribute $e bindPassword     } r
	  puts [ format "%-5s %-20s %-50s"  " " bindPassword $r ]
          catch { $AdminConfig showAttribute $e hosts            } hosts
	  puts [ format "%-5s %-20s %-50s"  " " hosts $hosts ]
          catch { $AdminConfig showAttribute $e ignoreCase       } r
	  puts [ format "%-5s %-20s %-50s"  " " ignoreCase $r ]
          catch { $AdminConfig showAttribute $e limit            } r
	  puts [ format "%-5s %-20s %-50s"  " " limit $r ]
          catch { $AdminConfig showAttribute $e monitorInterval  } r
	  puts [ format "%-5s %-20s %-50s"  " " monitorInterval $r ]
          catch { $AdminConfig showAttribute $e properties       } r
	  puts [ format "%-5s %-20s %-50s"  " " properties $r ]
          catch { $AdminConfig showAttribute $e realm            } r
	  puts [ format "%-5s %-20s %-50s"  " " realm $r ]
          catch { $AdminConfig showAttribute $e type             } r
	  puts [ format "%-5s %-20s %-50s"  " " type $r  ]
          catch { $AdminConfig showAttribute $e reuseConnection  } r
	  puts [ format "%-5s %-20s %-50s"  " " reuseConnection $r ]
          catch { $AdminConfig showAttribute $e searchTimeout    } r
	  puts [ format "%-5s %-20s %-50s"  " " searchTimeout $r ]
          catch { $AdminConfig showAttribute $e serverId         } r
	  puts [ format "%-5s %-20s %-50s"  " " serverId $r ]
          catch { $AdminConfig showAttribute $e serverPassword   } r
	  puts [ format "%-5s %-20s %-50s"  " " serverPassword $r ]
          catch { $AdminConfig showAttribute $e sslConfig        } r
	  puts [ format "%-5s %-20s %-50s"  " " sslConfig $r ]
          catch { $AdminConfig showAttribute $e sslEnabled       } r
	  puts [ format "%-5s %-20s %-50s\n"  " " sslEnabled $r ]

          catch { $AdminConfig showAttribute $e searchFilter     } LDAPSearchFilterId
	  puts [ format "%-5s %-20s %-50s"  " " LDAPSearchFilterId $LDAPSearchFilterId ]

	  catch { getLDAPSearchFilter $LDAPSearchFilterId } r

          lappend hostList $hosts 
    
       }	      

    } else {
 
        puts "\nproblem accessing LDAP user registry ID.\n"
        puts $r 
        puts "************************************\n"
        return -code error $r

    }

   lappend registryList $LDAPUserRegistryId 

   return [ list $registryList $hostList $LDAPSearchFilterId ]

}

#-------------------------------------------------------------------------------
# For existing LDAP server get search filter details.  
#-------------------------------------------------------------------------------

proc getLDAPSearchFilter { LDAPSearchFilterId } {

   global AdminConfig 

   puts "\n## List Ldap Search Filter ##\n" 

   foreach e $LDAPSearchFilterId {

      catch { $AdminConfig showAttribute $LDAPSearchFilterId certificateFilter } r
      puts [ format "%-5s %-20s %-50s"  " " certificateFilter $r ]
      catch { $AdminConfig showAttribute $LDAPSearchFilterId certificateMapMode} r
      puts [ format "%-5s %-20s %-50s"  " " certificateMapMode $r ]
      catch { $AdminConfig showAttribute $LDAPSearchFilterId groupFilter } r
      puts [ format "%-5s %-20s %-50s"  " " groupFilter $r ]
      catch { $AdminConfig showAttribute $LDAPSearchFilterId groupIdMap } r
      puts [ format "%-5s %-20s %-50s"  " " groupIdMap $r ]
      catch { $AdminConfig showAttribute $LDAPSearchFilterId groupMemberIdMap } r
      puts [ format "%-5s %-20s %-50s"  " " groupMemberIdMap $r ]
      catch { $AdminConfig showAttribute $LDAPSearchFilterId userFilter } r
      puts [ format "%-5s %-20s %-50s"  " " userFilter $r ]
      catch { $AdminConfig showAttribute $LDAPSearchFilterId userIdMap } r
      puts [ format "%-5s %-20s %-50s"  " " userIdMap $r ]

   }	      

}

#-------------------------------------------------------------------------------
# Delete any existing ldap host server definitions before defining a new one. 
#-------------------------------------------------------------------------------

proc deleteHosts { hosts } {

   global AdminConfig 

   puts "\n## Delete Existing Hosts ##\n" 

   # delete existing ldap host server ids or host modification will duplicate ids. 
   # extract host sublist from list 

   set hosts [ join $hosts ]

   foreach hostId $hosts {

      if { [ catch { $AdminConfig remove $hostId } r ] == 0 } {

	   puts  [ format "%-5s %-20s %-50s" " "  "Removed hostId"  $hostId ]
	   return $r

	   } else {

	   puts "\nproblem removing host $hostId. \n"
	   puts $r 
	   puts "************************************\n"
	   return -code error $r

      }
   }
}

#-------------------------------------------------------------------------------
# setup attribute values for LDAPUserRegistry using LDAPUserRegistry ConfigId
#-------------------------------------------------------------------------------

proc doLDAPUserRegistry { ldapServer   \
                          ldapServerId \
                          ldapPassword \
                          ldapPort     \
                          domainHostname \
                          baseDN \
                          LDAPUserRegistryId \
                          LDAPSearchFilterId } {

   global AdminConfig 

   puts "\n## Modify LDAP Registry Details ##\n" 

   set serverId        [ list serverId        $ldapServerId          ]
   set serverPassword  [ list serverPassword  $ldapPassword          ]
   set realm           [ list realm           $ldapServer:$ldapPort  ]
   set type            [ list type            {CUSTOM}               ]
   set baseDN          [ list baseDN          $baseDN                ]
   set reuseConnection [ list reuseConnection true                   ]
   set ignoreCase      [ list ignoreCase      true                   ]

   set host            [ list host $ldapServer     ]
   set port            [ list port $ldapPort       ]
   set hostsList       [ list [ list $host $port ] ]
   set hosts           [ list hosts $hostsList     ]

   set attrs [ list $serverId        \
                    $serverPassword  \
                    $realm           \
                    $type            \
                    $baseDN          \
                    $reuseConnection \
                    $ignoreCase      \
                    $hosts     
	     ]

   puts " ATTRS = $attrs"

   if { [ catch { $AdminConfig modify $LDAPUserRegistryId $attrs } r ] == 0 } {

       return $r

       } else {

       puts "\nproblem updating LDAP $LDAPUserRegistryId. \n"
       puts $r 
       puts "************************************\n"
       return -code error $r

   }

}

#-------------------------------------------------------------------------------
# setup attribute values for LDAPSearchFilterId using LDAPSearchFilterId ConfigId
#-------------------------------------------------------------------------------

proc modifyLDAPSearchFilterId { certificateMapMode \
				groupFilter \
				groupIdMap  \
				groupMemberIdMap \
				userFilter \
				userIdMap  \
				LDAPSearchFilterId } {

   global AdminConfig 

   puts "\n## Modify LDAP Filter Details ##\n" 

   # ldap mappings are [listed] to avoid special character quoting problems.

   set  certificateMapMode  [ list  certificateMapMode  [ join $certificateMapMode ] ]
   set  groupFilter         [ list  groupFilter         [ join $groupFilter        ] ]
   set  groupIdMap          [ list  groupIdMap          [ join $groupIdMap         ] ]
   set  groupMemberIdMap    [ list  groupMemberIdMap    [ join $groupMemberIdMap   ] ]
   set  userFilter          [ list  userFilter          [ join $userFilter         ] ]
   set  userIdMap           [ list  userIdMap           [ join $userIdMap          ] ]

   set attrs [ list $certificateMapMode \
                    $groupFilter        \
                    $groupIdMap         \
                    $groupMemberIdMap   \
                    $userFilter         \
                    $userIdMap          
	     ]

   if { [ catch { $AdminConfig modify $LDAPSearchFilterId $attrs } r ] == 0 } {

       return $r

       } else {

       puts "\nproblem updating LDAP $LDAPSearchFilterId. \n"
       puts $r 
       puts "************************************\n"
       return -code error $r

   }

}

####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 5} {
        return -code error "error - no arguments supplied.  Supply server name"
        puts "no arguments"
}

# if the ldap search mappings contain system characters [ list ] mappings.

set ldapServer           [ lindex $argv 0 ]
set ldapServerId         [ lindex $argv 1 ]
set ldapPassword         [ lindex $argv 2 ]
set ldapPort             [ lindex $argv 3 ]
set domainHostname       [ lindex $argv 4 ]
set baseDN               [ lindex $argv 5 ]

set certificateMapMode "EXACT_DN"
set groupFilter "(&(|(|(objectclass=groupOfNames)(objectclass=groupOfUniqueNames)(objectclass=top))(objectclass=groupOfURLs))(cn=%v))"
set groupIdMap "*:cn"
set groupMemberIdMap "groupOfNames:member;groupOfUniqueNames:uniqueMember"
set userFilter "(&(cn=%v)(|(objectclass=ABC)(objectclass=DEF)(objectclass=person)))"
set userIdMap "*.cn"

set nodeName [ $AdminControl getNode ]
set cellName [ $AdminControl getCell ]

puts "ldapServer      =  $ldapServer     "
puts "ldapServerId    =  $ldapServerId   "
puts "ldapPassword    =  $ldapPassword   "
puts "ldapPort        =  $ldapPort       "
puts "domainHostname  =  $domainHostname "
puts "baseDN          =  $baseDN         "
puts "nodeName        =  $nodeName       "
puts "cellName        =  $cellName       "

puts "certificateMapMode =  $certificateMapMode "
puts "groupFilter        =  $groupFilter        "
puts "groupIdMap         =  $groupIdMap         "
puts "groupMemberIdMap   =  $groupMemberIdMap   "
puts "userFilter         =  $userFilter         "
puts "userIdMap          =  $userIdMap          "

#######################################################################
# If the ldap server host definition already exists do not delete because it may be in use by some of the installed applications. Modify instead.
#######################################################################

if { [ catch { getLDAPUserRegistryId } r ] == 0 } {

    puts "\n Registry $r \n"

    set LDAPUserRegistryId [ lindex [ lindex $r 0 ] 0 ] 
    set hostList           [ lindex $r 1 ] 
    set LDAPSearchFilterId [ lindex $r 2 ] 

} else {
        return -code error $r 
}

# if the host list contains no elements or only null elements skip delete.

#puts "\n hostlist = $hostList \n" 

if { [ lindex [ eval join $hostList ] 0 ] == "" }  {
   puts "\nno hosts\n"
   set continue true 
} else {
    if { [ catch { deleteHosts $hostList } r ] == 0 } {
	 set continue true 
	 } else {
	 return -code error $r
    }
}

if { [ catch { doLDAPUserRegistry $ldapServer         \
                                  $ldapServerId       \
                                  $ldapPassword       \
                                  $ldapPort           \
                                  $domainHostname     \
                                  $baseDN             \
                                  $LDAPUserRegistryId \
                                  $LDAPSearchFilterId   \
} r ] == 0 } {

    if { [ catch { modifyLDAPSearchFilterId $certificateMapMode \
	                                    $groupFilter \
	                                    $groupIdMap \
	                                    $groupMemberIdMap \
	                                    $userFilter \
	                                    $userIdMap \
                                            $LDAPSearchFilterId } r ] == 0 } {

	puts "\n## Admin Config Save ##\n"
	catch { $AdminConfig save } r
	puts $r

    } else {
	    return -code error $r 
    }

} else {
        return -code error $r 
}

####################################################################
# List servers to verify install.
####################################################################

if { [ catch { getLDAPUserRegistryId } r ] == 0 } {
    set continue true
} else {
        return -code error $r 
}
