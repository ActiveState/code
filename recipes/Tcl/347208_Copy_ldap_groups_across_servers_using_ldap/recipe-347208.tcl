##############################################################
# Copy members from Lotus Domino groups to Tivoli LDAP groups.  
##############################################################

puts "\n executing [info script]\n"

# make script drive independent.

set drive [lindex [file split [info script]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

source [ file join $drive /scripts/TCL/proclib/checkFile_proc.tcl    ]
source [ file join $drive /scripts/TCL/proclib/smtp_proc.tcl         ]
source [ file join $drive /scripts/TCL/proclib/netSend_proc.tcl      ]
source [ file join $drive /scripts/TCL/proclib/reportHeader_proc.tcl ]

package require ldap 

###########################################
# Get the members of the group from Lotus 
# For each Lotus member get the UID 
# Get the base dn of the groups in ldap 
# Get the base dn of the corresponding member in ldap
# Update the ldap group. 
###########################################

proc replicateGroups { groupList s1 s2 bindDn pw reportFileId attr } {

    global sourceServer 
    global targetServer

    # group membership information is returned as given name and surname.
    # Get the uid using given name and surname.

    foreach { x } $groupList {

       puts               [ format "\n%-30s %s" { } {***********} ]
       puts $reportFileId [ format "\n%-30s %s" { } {***********} ]

       puts "\nMapping persons from \"[lindex $x 0 ]\" on Lotus to  \"[lindex $x 1 ]\"\.\n"
       puts $reportFileId "\nMapping persons from \"[lindex $x 0 ]\" on Lotus to \"[lindex $x 1 ]\"\.\n"

       set sourceGroupCn (cn=[lindex $x 0 ])
 
       # search from the root dse by using a null string for the base option. 

       if { [ catch { ldap::search $sourceServer "" "$sourceGroupCn" {member} } r ] == 0 } {

           # search returns null if no matches.

	   foreach i [ lindex $r 0 1 1 ]  { 

	       set cn [ string trimright $i {,o=ABC} ] 

	       set uid [ lindex [ ldap::search $sourceServer "o=ABC" ($cn) {uid} ] 0 1 1 ]

               # Lotus Notes Ldap groups may contain members that no longer exist in Lotus Schema hence uid may be null string.  

               if { [ string is space -strict $uid ] == 1 || $uid == {} } {
                   puts $reportFileId "############### Error"
                   puts $reportFileId "############### $cn does not exist in Lotus Notes"
               } else {
		       lappend cnList cn\=$uid 
		       unset uid
               }

           }
	      
       } else {

	       puts "r = $r" 

	       puts $reportFileId $r 

	       return -code error $r 

       }

       # skip this loop if the source group is null(not found). 

       if { [ info exist cnList ]  == 1 } {

          # build ldap entry for the IBM ldap group 

	   set targetGroupCn (cn=[lindex $x 1 ])
	   
	  # get the full dn of the target group.

	   set baseDnGroup [ lindex [ ldap::search $targetServer "o=ABC,dc=com.au,c=au" "$targetGroupCn" {cn} ]  0 0 ]

	  # call proc process person to move members to group.

	   processPerson $reportFileId $baseDnGroup $cnList $attr

       } else {

               puts "\n$sourceGroupCn does not exist on Lotus server $s1\."
               puts $reportFileId "\n$sourceGroupCn does not exist on ldap server $s1\."

       }
    }
}

###########################################
# Get the members of the group from Lotus 
# For each Lotus member get the UID 
###########################################
proc processPerson { reportFileId baseDnGroup cnList attr } {

   global sourceServer 
   global targetServer

    
   foreach i $cnList {

      # get the full dn of the target person.
      # we assume that the target person is already in the ldap schema but not in the group. 
      # NB the cn of the target person must be unique in the schema. 
      # NB the cn must exist in the schema. 
       
      set baseDnPerson [ lindex [ ldap::search $targetServer "o=ABC,dc=com.au,c=au" "($i)" {cn}] 0 0 ]
      
      if { [ string is space -strict $baseDnPerson ] == 1 || $baseDnPerson == {} } {

          puts $reportFileId "\n############### Error"
          puts $reportFileId "############### $i does not exist in IBM Ldap"

      } else {

	 # check whether the person is already a member of the group

	 set memberOf [ lindex [ ldap::search $targetServer "o=ABC,dc=com.au,c=au" "($i)" {ibm-allGroups} ] 0 1 1 ]

	 if { [ lsearch -regexp $memberOf "(?ni)$baseDnGroup" ] != -1 } {

             puts "\nEntry $baseDnPerson is already a member of $baseDnGroup" 
             puts $reportFileId "\nEntry $baseDnPerson is already a member of $baseDnGroup"
         } else {

	     puts "\nAdd $baseDnPerson to $baseDnGroup" 
	     puts $reportFileId "\nAdd $baseDnPerson to $baseDnGroup" 

	     puts "\nldap::modify $targetServer $baseDnGroup {} {} [ list $attr $baseDnPerson ] "
	     if { [ catch { [ ldap::modify $targetServer $baseDnGroup {} {} [ list $attr $baseDnPerson ] ] } r ] == 0 } {
		 puts "\n$baseDnPerson added to $baseDnGroup" 
		 puts $reportFileId "\n$baseDnPerson added to $baseDnGroup" 
	     } else {
		 puts "\n$r" 
		 puts $reportFileId "\n$r"
	     }
         }
      }
   }
}
###########################################
# Email Report 
###########################################

proc emailReport { reportFile reportFileId } {

   flush $reportFileId  

   set computerName $::env(COMPUTERNAME)
   set subject "$computerName - Lotus - LDAP Replication"   
   sendSimpleMessage youremail@xxx.com $subject $reportFile

}
######################################
# Control Section. 
######################################

######################################
# Set Variables
######################################

set fileDate [ clock format [ clock seconds ] -format %Y-%m-%d_%H.%M.%S ]

set reportFile  [ file join $drive reports/ldap/lotusReplicationGroups_$fileDate\.txt ]

set s1      xxxxxxx
set s2      yyyyyyy
set bindDn  "cn=frrfr" 
set pw      password
set attr    uniqueMember 

puts "\ns1 = $s1"
puts "s2 = $s2\n"
puts "reportfile    = $reportFile\n"

######################################
# Report Header. 
######################################

set reportFileId [ open $reportFile w ]
set header       "$::env(COMPUTERNAME) - Lotus LDAP Replication"
set baseDN       "ou=ldapgroups,o=ABC,dc=com.au,c=au" 
reportHeader     $reportFileId $header $reportFile

# map the Lotus Roles to the LDAP groups

lappend groupList [ list "DominoGroup 1"  LdapGroup1 ]
lappend groupList [ list "DominoGroup 2"  LdapGroup2 ]
lappend groupList [ list "DominoGroup 3"  LdapGroup3 ]
lappend groupList [ list "DominoGroup 4"  LdapGroup4 ]

# connect to ldap 

set sourceServer [ ldap::connect $s1 389 ]

::ldap::bind $sourceServer 

set targetServer [ ldap::connect $s2 389 ]

::ldap::bind $targetServer $bindDn $pw

global sourceServer
global targetServer

######################################
# Extract dominoPersons from Lotus. 
######################################

if { [ catch { replicateGroups $groupList $s1 $s2 $bindDn $pw $reportFileId $attr } r ] == 0 } {

   puts "\nr = $r" 

   } else { 

   puts "\n = $r" 
   puts $reportFileId \n$r 

} 

::ldap::unbind $sourceServer 
::ldap::unbind $targetServer 
::ldap::disconnect $sourceServer 
::ldap::disconnect $targetServer 

emailReport $reportFile $reportFileId

close $reportFileId

######################################
# END.
######################################
