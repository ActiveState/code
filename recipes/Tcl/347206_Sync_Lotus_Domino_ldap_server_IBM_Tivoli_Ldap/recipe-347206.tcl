########################################################  
# Sync Tivoli Directory Server from Lotus Notes Domino.  
# Add new Lotus Notes entries to Tivoli. 
# Delete old Lotus Notes entries from Tivoli and remove entries from roles. 
# Write report and email to respondents. 
########################################################  

puts "\n executing [info script]\n"

# make script drive independent.

set drive [lindex [file split [info script]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

########################################################  
# Source utility procs.
########################################################  

source [ file join $drive /scripts/TCL/proclib/checkFile_proc.tcl    ]
source [ file join $drive /scripts/TCL/proclib/smtp_proc.tcl         ]
source [ file join $drive /scripts/TCL/proclib/netSend_proc.tcl      ]
source [ file join $drive /scripts/TCL/proclib/reportHeader_proc.tcl ]

########################################################  
# Source packages. 
########################################################  

package require ldap 
package require Tclx 

###########################################
# Toplevel Proc.
###########################################
proc topProc { reportFileId attr } {

    if { [ catch { extractDominoPersons } r ] == 0 } {

       set dominoPersons $r

       } else { 

       return -code error    $r

    } 

    #############################################
    # Extract internal users from IBM ldap. 
    #############################################

    if { [ catch { extractldapPersons } r ] == 0 } {

       set ldapPersons $r

       } else { 

       return -code error    $r

    } 

    #####################################################################################
    # compare users - extract and delete the entries that exist in ldap but not in Lotus.
    #####################################################################################

    if { [ catch { diffPersons $dominoPersons $ldapPersons $attr } r ] == 0 } {

       puts $r 

       } else { 

       puts $r
       return -code error $r 

    } 
}
###########################################
# Extract dominoPersons from Lotus ldap 
###########################################
proc extractDominoPersons {} {

    global s1 
    global lotusBaseDN

    # Search on objectclass.  Return uid.
    # Return sorted list 
    
    set filter [ list "objectClass=dominoPerson" ]
    
    if { [ catch { ldap::search $s1 $lotusBaseDN $filter {uid} } r ] == 0 } {

	return [ lsort $r ]
	
    } else {

	return -code error $r

    }

}
###########################################
# Extract Internal Users from IBM ldap.
###########################################
proc extractldapPersons {} {

    global s2 
    global ldapBaseDN 

    # Search on objectclass.  Return cn.
    # Return sorted list 

    set filter [ list "objectClass=ldapPerson" ]
    
    if { [ catch { ldap::search $s2 $ldapBaseDN $filter {cn} } r ] == 0 } {

	return [ lsort $r ]
	
    } else {

	return -code error $r

    }

}
###########################################
# Diff Entries.
###########################################
proc diffPersons { dominoPersons ldapPersons attr } {

    global reportFileId
    global ldapServer

    set x 0

    # Extract Domino Uids. 

    foreach i $dominoPersons {
	lappend dominoPersonsList [ lindex $dominoPersons $x 1 1 0 ]
	incr x
    }

    set x 0

    # Extract Tivoli Cns. 
   
    foreach i $ldapPersons {
        lappend ldapPersonsList [ lindex $ldapPersons $x 1 1 0 ]
        incr x
    }

    # Threeway match. 

    foreach { x y z } [ lindex [ intersect3 $dominoPersonsList $ldapPersonsList ] ] {

	set addPersons      $x 
	set matchingPersons $y
	set deletePersons   $z 

    }

    # If the lists are null skip add/delete steps.
    
    set p1 "*****************************************"
    set p2 "* No persons to add"
    set p3 "* No persons to delete"

    # add Domino entry to Tivoli
    
    if { $addPersons == {} || [ string is space $addPersons ] } {

	set t1 [ format "%-20s %s"  " " $p1 ]
	set t2 [ format "%-20s %-30s"  " " $p2 ] 

	puts                \n$t1
	puts                $t2
	puts                $t1\n

	puts  $reportFileId \n$t1
	puts  $reportFileId $t2
	puts  $reportFileId $t1\n
    
    } else {

	    if { [ catch { addPersons $addPersons } r ] == 0 } {

	       set continue true 

	       } else { 

	       return -code error    $r

	    } 

    }

    # delete entry from Tivoli

    if { $deletePersons == {} || [ string is space $deletePersons ] } {

	set t1 [ format "%-20s %s"    " " $p1 ]
	set t2 [ format "%-20s %-30s"  " " $p3 ]

	puts                \n$t1
	puts                $t2
	puts                $t1\n

	puts  $reportFileId \n$t1
	puts  $reportFileId $t2
	puts  $reportFileId $t1\n
    
    } else {

	    if { [ catch { deletePersons   $deletePersons } r ] == 0 } {

	       set continue true 

	       } else { 

	       return -code error    $r

	    } 

    }

}
######################################################################
# Add Persons.
# Add entries which exist on Lotus Domino but do not exist on Tivoli.
######################################################################
proc addPersons { addPersons } {

    global s1
    global s2
    global reportFileId
    global ldapBaseDN
    global lotusBaseDN
    global ldapServer
    global bindDN
    global pw

    set addCount [ llength $addPersons ]

    set p1 "*****************************************"
    set p2 "* Adding Lotus Persons to LDAP"
    set p4 "* Add count is $addCount"

    set t1 [ format "%-20s %30s"  " " $p1 ]
    set t2 [ format "%-20s %-30s" " " $p2 ] 
    set t7 [ format "%-20s %-30s" " " $p4 ] 
    
    puts                $t1
    puts                $t2
    puts                $t7
    puts                $t1
    
    puts  $reportFileId $t1
    puts  $reportFileId $t2
    puts  $reportFileId $t7
    puts  $reportFileId $t1
    
    foreach i $addPersons {

	# select the required attributes from lotus. 

	set filter     "(uid=$i)"
	set attributes {cn givenname sn mail}

	if { [ catch { ldap::search $s1 $lotusBaseDN $filter $attributes } results ] == 0 } {

	   set dn cn=$i\,$ldapBaseDN

	   set objectclass1 top
	   set objectclass2 person
	   set objectclass3 organizationalPerson
	   set objectclass4 inetOrgPerson
	   set objectclass5 ldapPerson
		  
	   # Domino entries may have invalid fields. 
	   # Data cleanup is required.

	   set   cn        $i
	   set   uid       $i

	   set sList [ lindex $results 0 1 ] 

	   if { [ lsearch $sList {*givenname*} ] == -1 } {
	        set givenname "$i" 
	   } else {
	       set index     [ lsearch $sList {*givenname*} ]
               set givenname [ lindex  $sList [ incr index ]]
               unset index 
	   }

	   if { [ lsearch $sList {*sn*} ] == -1 } {
	        set sn "$i" 
	   } else {
               set   index   [ lsearch $sList {*sn*} ]
               set   sn      [ lindex  $sList [ incr index ]]
               unset index 
	   }
	   
	   if { [ lsearch $sList {*mail*} ] == -1 } {
	        set mail "$i" 
	   } else {
	       set   index  [ lsearch $sList {*mail*} ]
	       set   mail   [ lindex $sList [ incr index ] ]
	       unset index 
	   }

	   set userPassword "password"                

           # build attribute list 

	   set list1 [ list objectclass ldapPerson      \
			    objectclass inetOrgPerson  \
			    objectclass organizationalPerson \
			    objectclass person         \
			    objectclass top            \
			    cn $cn                     \
			    uid $uid                   \
			    sn $sn                     \
			    givenname $givenname       \
			    mail $mail                 \
			    userPassword $userPassword ]

	   set g [ string trimleft $givenname givenname= ] 
	   set s [ string trimleft $sn sn= ] 
	   set c [ string trimleft $cn cn= ] 

	   set width [ string length "$s $g \($c\)" ]   

	   set t1 [ format "\n%s %-${width}s %s"  "Adding" "$s $g \($c\)" "to $ldapServer" ]
	   set t2 [ format "\n%s %-${width}s %s"  "   Added" "$s $g \($c\) " "to $ldapServer" ]
	   set t3 [ format "%s"  "   $dn" ]
	   set t4 [ format "\n%s %-${width}s %s"  "   Error adding" "$s $g \($c\) " "to $ldapServer" ]
	   set r "" 
	   set t5 [ format "%s"  "   $r" ]

	   puts                $t1
	   puts                $t3 
	   puts  $reportFileId $t1
	       
           # add entry 
	    
	   if { [ catch { ldap::add $s2 $dn $list1 } r ] == 0 } {

	      puts                $t2
	      puts                $t3 
	      puts  $reportFileId $t2
	      puts  $reportFileId $t3 


           } else {

	       puts                $t4
	       puts                $t3 
	       puts                $t5 
	       puts  $reportFileId $t4
	       puts  $reportFileId $t3
	       puts  [ format "%s"  "   $r" ]
	       puts  $reportFileId [ format "%s"  "   $r" ]

           } 

	   unset dn
	   unset objectclass5
	   unset objectclass4
	   unset objectclass3
	   unset objectclass2
	   unset objectclass1

	   unset cn
	   unset uid
	   unset sn
	   unset givenname
	   unset mail
	   unset userPassword

	   unset list1

	}

    }
}
######################################################################
# Delete Persons.
# Delete entries from Tivoli which exist on Domino but do not exist on Tivoli.
######################################################################
proc deletePersons { deletePersons } {

    global s1
    global s2
    global reportFileId
    global ldapBaseDN
    global attr
    global ldapServer

    set deleteCount [ llength $deletePersons ]

    set p1 "*****************************************"
    set p2 "* Deleting Lotus Persons from LDAP"
    set p4 "* Delete count is $deleteCount"

    set t1 [ format "%-20s %30s"  " " $p1 ]
    set t2 [ format "%-20s %-30s" " " $p2 ] 
    set t7 [ format "%-20s %-30s" " " $p4 ] 
    
    puts                \n$t1
    puts                $t2
    puts                $t7
    puts                $t1
    
    puts  $reportFileId \n$t1
    puts  $reportFileId $t2
    puts  $reportFileId $t7
    puts  $reportFileId $t1

    foreach i $deletePersons {

        # Get the full dn of the target person.
        # Search on CN.

        set attrs [ ldap::search $s2 $ldapBaseDN "(cn=$i)" { cn givenname sn } ] 

        set baseDNPerson [ lindex $attrs 0 0 ]
        set g            [ lindex $attrs 0 1 1 ]
        set s            [ lindex $attrs 0 1 3 ]

	set y "$s $g \($i\)"   
	
	set width [ string length $y ]   

	set t1 [ format "\n%s %-${width}s %s"  "Deleting " $y "from $ldapServer" ]
	set t2 [ format "\n%s %-${width}s %s"  "   Deleted " $y "from $ldapServer" ]
	set t3 [ format "%s"  "   $baseDNPerson" ]
	set t4 [ format "\n%s %-${width}s %s"  "   Error deleting " $y "from $ldapServer" ]
	set r "" 
	set t5 [ format "%s"  "   $r" ]

        # get the roles assigned to the target person.

        set memberOf [ lindex [ ldap::search $s2 $ldapBaseDN "(cn=$i)" {ibm-allGroups} ] 0 1 1 ]

	set replace {}
	set delete  [ list $attr $baseDNPerson ]
	set add     {}

        # remove the target person from roles. 

	foreach i $memberOf {

	   set t6 [ format "\n%s %-${width}s %s"  "Removing " $y "from $i" ]

	   puts                $t6 
	   puts  $reportFileId $t6

	   if { [ catch { ldap::modify $s2 $i $replace $delete $add } r ] == 0 } {

	       set t6 [ format "\n%s %-${width}s %s"  "Removed " $y "from $i" ]

	       puts                $t6
	       puts  $reportFileId $t6

	   } else {

	       set t6 [ format "\n%s %-${width}s %s"  "Error removing " $y "from $i" ]

	       puts                $t6 
	       puts  $reportFileId $t6
	       puts  [ format "%s"  "   $r" ]
	       puts  $reportFileId [ format "%s"  "   $r" ]

	   }
      
        }

        # delete the target person 

	puts                $t1
	puts                $t3 
	puts  $reportFileId $t1

	if { [ catch { ldap::delete $s2 $baseDNPerson } r ] == 0 } {

 	    puts                $t2
 	    puts                $t3 
 	    puts  $reportFileId $t2
 	    puts  $reportFileId $t3 
 
	} else {

	       puts                $t4
	       puts                $t3 
	       puts                $t5 
	       puts  $reportFileId $t4
	       puts  $reportFileId $t3
	       puts  [ format "%s"  "   $r" ]
	       puts  $reportFileId [ format "%s"  "   $r" ]

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
   sendSimpleMessage xxx@xxx.com $subject $reportFile

}
######################################
# Control Section.
######################################

######################################
# Set Variables.
######################################

set fileDate    [ clock format [ clock seconds ] -format %Y-%m-%d_%H-%M-%S ]

set reportFile  [ file join $drive reports/ldap/lotusSync_$fileDate\.txt ]

set lotusServer xxxxx 
set ldapServer  yyyyy 
set bindDN      "cn=xxxxx" 
set pw          yxyxyx 
set attr        uniqueMember 

puts "reportfile    = $reportFile\n"

######################################
# Report Header. 
######################################

set reportFileId [ open $reportFile w ]
set header       "$::env(COMPUTERNAME) - Lotus LDAP Replication"
set ldapBaseDN   "ou=xxxxxxx,o=yyyyy,dc=com.au,c=au" 
set lotusBaseDN  "o=aaa" 

reportHeader $reportFileId $header $reportFile

puts               [ format "%-15s %s %s" "Lotus Server"  "- " $lotusServer ]    
puts               [ format "%-15s %s %s" "Tivoli Server" "- " $ldapServer ]    
puts $reportFileId [ format "%-15s %s %s" "Lotus Server" "- " $lotusServer ]    
puts $reportFileId [ format "%-15s %s %s" "Tivoli Server" "- " $ldapServer ]    

################################### 
# Connect and bind to ldap servers
################################### 

set s1 [ ldap::connect $lotusServer 389 ]

::ldap::bind $s1 

set s2 [ ldap::connect $ldapServer 389 ]

::ldap::bind $s2 $bindDN $pw

################################### 
# Global variables.
################################### 

global s1
global s2 
global reportFileId
global ldapBaseDN 
global lotusBaseDN 
global ldapServer 
global bindDN

######################################
# Call toplevel proc. 
######################################

if { [ catch { topProc $reportFileId $attr } r ] == 0 } {

      puts $r 

      } else { 

      puts $r
      puts $reportFileId $r

}

#############################################
# Write Report footer. 
#############################################

set s "*****************************************"
set t1 [ format "%-20s %s" " " $s ]
set s "The End"
set t2 [ format "%-35s    %s" " " $s ]

puts                \n$t1
puts                $t2 
puts                $t1

puts  $reportFileId \n$t1
puts  $reportFileId $t2
puts  $reportFileId $t1

##########################################
# Unbind and disconnect from ldap servers
########################################## 

::ldap::unbind $s1 
::ldap::unbind $s2
::ldap::disconnect $s1
::ldap::disconnect $s2

emailReport $reportFile $reportFileId 
    
close       $reportFileId

######################################
# END.
######################################
