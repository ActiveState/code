###########################################################
# Check available drive space. 
# Email alert if space usage exceeds 90%.
###########################################################

puts "\n executing [info script]\n"

# make script drive independent.

set drive [lindex [file split [info nameofexecutable]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

########################################################  
# Source utility procs.
########################################################  

source [ file join  $drive scripts/TCL/proclib/checkFile_proc.tcl ]
source [ file join  $drive scripts/TCL/proclib/smtp_proc.tcl ]
source [ file join  $drive scripts/TCL/proclib/reportHeader_proc.tcl ]
source [ file join  $drive scripts/TCL/proclib/printColumns.tcl ]
source [ file join  $drive scripts/TCL/proclib/convertToMb.tcl ]

########################################################  
# Source packages. 
########################################################  

package require twapi
package require Tclx
package require math::fuzzy
package require textutil

######################################
# Proc - check memory usage. 
######################################
proc driveSpace {} {

   puts "\n driveSpace \n"

   # calculate drive size and free space.  

   set drives [ concat [ twapi::get_logical_drives -type fixed ] \
                       [ twapi::get_logical_drives -type remote ]
	      ]

   foreach d $drives {

      array set a    [ twapi::get_drive_info $d -size -freespace ] 

      set spaceUsed  [ expr { (double ( $a(-size) - $a(-freespace) )/ $a(-size) ) } ] 

      set usedPerc   [ expr { [math::fuzzy::troundn $spaceUsed 2] *100 } ]

      set driveSize  [ concat [ toMB $a(-size) ]MB ]

      set driveSpace [ concat [ toMB $a(-freespace) ]MB ]

      lappend driveInfo [ list $d $driveSize $driveSpace $usedPerc ]

   }


#   if space usage is > 90 send error report.

   foreach e $driveInfo {

       if { [ lindex $e 3 ] > 90 } { 

	  set alert true 

       } else {

	  set alert false 

       }

   }

   if { [ string is true $alert ] } {
   
      writeReport $driveInfo
      
   }
   
}

######################################
# Proc - write report
######################################
proc writeReport { driveInfo } {
  
   global reportFile
   global reportFileId

   set header       "$::env(COMPUTERNAME) - Check Drive Space Usage"

   reportHeader $reportFileId $header $reportFile

   set s "*****************************************"
   set t1 [ format "%-15s %s" " " $s ]
   set s "The End"
   set t2 [ format "%-35s    %s" " " $s ]
   set t3 "$::env(COMPUTERNAME) - Space utilization." 

   puts $reportFileId \n$t3\n

   set width 12 
   set space " " 

   # format column headers in 12 character columns justified center. 

   set x [ list Drive  Size  FreeSpace  UsedPerc ] 

   foreach e $x {

      set c [ textutil::adjust $e -length $width -justify center -full true ]

      lappend lineH $c

   }

   set formatString "%-15s %s\n"
   
   puts $reportFileId [ format $formatString $space [ join $lineH ] ]
   
   set formatString "%-15s [ string repeat {%s } 4 ]" 
   
   # format detail line in 12 character columns with drive letter justified center and numerics justified right.

   foreach e $driveInfo {

       set driveLetter [ lindex $e 0 ]

       set c [ textutil::adjust $driveLetter -length $width -justify center -full true ]
        
       lappend line1 $c

       set y [ lrange $e 1 end ]

       foreach e $y {

          set c [ textutil::adjust $e -length $width -justify right ]

	  lappend line1 $c

       }

      set formatString "%-15s %s"

      puts $reportFileId [ format $formatString $space [ join $line1 ] ]

      unset line1
   }

   emailReport 

   ftruncate -fileid $reportFileId 0
}
###########################################
# Email Report 
###########################################

proc emailReport {} {

   global reportFile
   global reportFileId

   flush $reportFileId  

   set computerName $::env(COMPUTERNAME)

   set subject "$computerName - DriveSpace Alert."   

   sendSimpleMessage you@yourmail.com $subject $reportFile

}
######################################
# Control Section.
######################################

######################################
# Set Variables
######################################

set processId [ twapi::get_current_process_id ]

set eventId   [ twapi::eventlog_open -write ]

set data "DRIVESPACE STARTING"

twapi::eventlog_write $eventId 1 -type information -loguser -data $data

twapi::eventlog_close $eventId

set reportFile   [ file join $drive reports/notify/driveSpace.txt ]

#########################################
# Check if files exist.
#########################################

checkFile [file dirname $reportFile]

######################################
# Open output files.
######################################

set reportFileId  [open $reportFile w]

################################### 
# Global variables.
################################### 

global reportFile
global reportFileId

driveSpace
