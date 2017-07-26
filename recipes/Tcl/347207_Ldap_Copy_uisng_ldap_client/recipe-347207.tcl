####################################################  
# Copy Lotus Domino entries to IBM Tivoli ldap server.  
# Uses "exec" to shell out to ldap client utilities rather than using ldap package. 
####################################################  

puts "\n executing [info script]\n"

# make script drive independent.

set drive [lindex [file split [info script]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

source [ file join $drive /scripts/TCL/proclib/checkFile_proc.tcl    ]
source [ file join $drive /scripts/TCL/proclib/smtp_proc.tcl         ]
source [ file join $drive /scripts/TCL/proclib/netSend_proc.tcl      ]
source [ file join $drive /scripts/TCL/proclib/reportHeader_proc.tcl ]

###########################################
# Extract dominoPersons from Lotus ldap 
###########################################
proc extractDominoPersons { lotusServer } {

    if {[catch {exec ldapsearch -h $lotusServer -v -b "o=xxx" "objectclass=dominoPerson" uid cn sn givenname mail } r] == 0} {
        return $r
       } else {
	   return -code error $r
    }

}
##############################################################
# Load Tivoli Ldap server with Domino Persons.  
# Use textutil package to parse data into appropriate format.
##############################################################

proc importDominoPersons { ldapServer userid password reportFileId dominoPersons baseDN deleteFileId } {

    package require textutil

    set listed [ textutil::splitx $dominoPersons "CN=" ]

    # delete first element. 

    set listed [ lreplace $listed 0 0 ] 
    
    foreach dominoPerson $listed {

       set dominoPersonListed [ split $dominoPerson \n ]

       append cn cn= [ string trimleft [ lsearch -inline $dominoPersonListed {*uid*} ] "uid=" ] 
       set sn        [ lsearch -inline $dominoPersonListed {*sn=*} ] 
       set uid       [ lsearch -inline $dominoPersonListed {*uid*} ] 
       set givenName [ lsearch -inline $dominoPersonListed {*givenname*} ] 
       set mail      [ lsearch -inline $dominoPersonListed {*mail*} ] 

       set userPassword "userPassword=password"

       # set cn to the UID.
       
       #regexp {(uid=)(.*)} $uid match 1 2

       #set cn "cn=$2"

       puts  $deleteFileId "$cn\,$baseDN"

       flush $deleteFileId

       set objectclass1 top
       set objectclass2 person
       set objectclass3 organizationalPerson
       set objectclass4 inetOrgPerson
       set objectclass5 ldapPerson
	      
       lappend list1 "$cn\,$baseDN"
       lappend list1 "objectclass=$objectclass5" 
       lappend list1 "objectclass=$objectclass4"
       lappend list1 "objectclass=$objectclass3"
       lappend list1 "objectclass=$objectclass2"
       lappend list1 "objectclass=$objectclass1"
       lappend list1 "$cn"
       lappend list1 "$uid"
       lappend list1 "$sn"
       lappend list1 "$givenName"
       lappend list1 "$mail"
       lappend list1 "$userPassword"

       lappend ldifList $list1 
       
       unset list1
       unset cn
    }

    # If the entry already exists modify instead.

    foreach e $ldifList {
	
        set e [ join $e \n]

	puts $e

	if { [ catch {exec ldapadd -h $ldapServer -D $userid -w $password -c << $e } r ] == 0 } {

	         puts $r 
	         puts $reportFileId $r 

	        } else {

	         puts $r 
	         puts "ldap modify instead"  
	         puts $reportFileId $r 
	         puts $reportFileId "ldap modify instead"  

	         catch { exec ldapmodify -h $ldapServer -D $userid -w $password -c << $e } r  
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
# Control Section
######################################

######################################
# Set Variables
######################################

set reportFile  [ file join $drive reports/ldap/lotusReplication.txt ]
set deleteFile  [ file join $drive reports/ldap/lotusReplicationDelete_[clock seconds].txt ]
set lotusServer xxxxxxx
set ldapServer  yyyyyyy
set userid      "cn=xtxtxt" 
set password    yourpassword

puts "\nlotusServer = $lotusServer"
puts "ldapServer    = $ldapServer\n"
puts "reportfile    = $reportFile\n"
puts "deleteFile    = $deleteFile\n"

######################################
# Report Header. 
######################################

set reportFileId [ open $reportFile w ]
set deleteFileId [ open $deleteFile w ]
set header       "$::env(COMPUTERNAME) - Lotus LDAP Replication"
set baseDN       "ou=xxxx,o=yyyy,dc=com.au,c=au" 
reportHeader $reportFileId $header $reportFile

######################################
# Extract dominoPersons from Lotus. 
######################################

if { [ catch { extractDominoPersons $lotusServer } r ] == 0 } {

    set dominoPersons $r 

   } else { 

   puts "r = $r" 
   puts $reportFileId $r 

} 

#######################################
## Import dominoPersons to Ldap 
#######################################

if { [ catch { importDominoPersons $ldapServer $userid $password $reportFileId $dominoPersons $baseDN $deleteFileId } r ] == 0 } {

    set continue true 

   } else { 

   puts $reportFileId $r 
 
} 

puts "Report written to $reportFile"
puts $reportFileId "Report written to $reportFile"
puts $reportFileId "\n#################################################################"

emailReport $reportFile $reportFileId

close $reportFileId

######################################
# END.
######################################
