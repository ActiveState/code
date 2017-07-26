#################################################
# FTP Cloudscape DB to remote server - Recursive. 
#################################################

puts "\n executing [info script]\n"

# make script drive independent.

set drive [lindex [file split [info nameofexecutable]] 0 ] 

package require ftp
package require Tclx

######################################
# Get FTP Connection.
######################################
proc getFtp { host logon password transferType} {
    
    set ftp::VERBOSE 1

    set ftp::DEBUG 1

    puts  "\n **** getFtp_proc **** \n"

    set ftphandle [ ftp::Open $host $logon $password ]

    ftp::Type $ftphandle $transferType 

    return $ftphandle
    
}
##################################################################
# List the directories and files in the local nested directories.
##################################################################
proc getFiles { baseDir } {

    puts  "\n **** getFiles proc **** \n"

   # extract the sub directories from the base directory 

   set fileList [ recursive_glob $baseDir * ]

   foreach e $fileList { 

       if { [ file isdirectory $e ] } {

           lappend dList $e 

       } else {

           lappend fList $e 

       }

   }

   return [ list $dList $fList ] 

}
###############################################################
# Create the local directory structure on the remote server.
###############################################################
proc ftpDirsFiles { ftphandle files } {

   puts  "\n **** ftpDirsFiles proc **** \n"

   # create the remote directories. 
   # paths must be relative.  
 
   foreach i [ lindex $files 0 ] {

       set rd [ eval file join [ join [ lrange [ file split $i  ] 1 end ] ] ]

       puts "\n local dir: $i"
       puts "\n remotedir: $rd"

       ::ftp::MkDir $ftphandle $rd

   }

   # ftp the files. 
   # paths must be absolute on local server and relative on remote server.  

   unset i

   foreach i [ lindex $files 1 ] {

       set rf [ eval file join [ join [ lrange [ file split $i  ] 1 end ] ] ]

       puts "\n local file: $i"
       puts "\n remote file $rf"

       ::ftp::Put $ftphandle $i $rf 

   }

}
######################################
# Main Control.
######################################

set localDir   [ file join $drive CloudScapeDatabasesBackups ]
set host       ftphost
set logon      yourlogon
set password   yourpassword

set transferType binary 

puts "\n localDir   = $localDir"

# get FTP connection

if { [ catch { getFtp $host $logon $password $transferType } r ] == 0 } {  

   puts "\n Connected to $host as $logon \n"  
   set ftpHandle $r 

} else {

   puts "\n Failed to connect to $host as $logon \n"  
   exit 1

}

ftpDirsFiles $ftpHandle [ getFiles $localDir ] 
