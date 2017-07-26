###########################################################
# Check for Maximum CPU usage. 
# Email alert if cpu exceeds 95%.
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
package require winutils
package require Tclx

######################################
# Proc - check cpu usage. 
######################################
proc checkCpu {} {

   puts "\n checkcpu \n"

   while {1} { 

      # pause for 30 seconds 

      after 30000

      # check processor utilization over a ten second interval.
       
      set cpu [lindex [twapi::get_processor_info 0 -processorutilization -interval 10000] 1]

#     if cpu is > 90% and alert has not been generated send error report.

      set cpu 95

      if { ![ info exist report ] } {
         
         set report false
         
      }
         
      if { [ expr { int($cpu) } ] > 90 && [ string is false $report ] } { 

	  set report true
          
          writeReport $cpu 

      } else {

	  set continue true 

      }

      # if cpu is < 90% and alert has been generated send OK report.

      if { [ expr { int($cpu) }  ] < 90 && [ string is true $report ] } { 

	  set report false

          writeReport $cpu 

      } else {

	  set continue true 

      }

   }

}
######################################
# Proc - write report
######################################
proc writeReport { cpu } {
  
   global reportFile
   global reportFileId

   set header       "$::env(COMPUTERNAME) - Check Cpu Alert"

   reportHeader $reportFileId $header $reportFile
 
   set s "*****************************************"
   set t1 [ format "%-20s %s" " " $s ]
   set s "The End"
   set t2 [ format "%-35s    %s" " " $s ]
   set t3 "$::env(COMPUTERNAME) -  CPU utilization is $cpu\%\. " 
   set t9 "CPU utilization - Top Ten" 

   puts $reportFileId \n$t3\n

   set s "*****************************************"
   set t1 [ format "%-20s %s" " " $s ]

   puts $reportFileId \n$t1
   puts $reportFileId [ format "%-20s %s" " " $t9 ]
   puts $reportFileId $t1\n

   foreach e [ processDetails ] {

       set spaces " "
       set processName [ lindex $e 0 0 ]
       set processId   [ lindex $e 0 1 ] 
       set cpuUsage    [ expr { int( [ lindex $e 1 ] ) } ]

       set width [ string length $processId ]
                                               
       puts $reportFileId [ format "%-20s %-20s %6s %3d" $spaces      \
                                                         $processName \
                                                         $processId   \
                                                         $cpuUsage ]

   }

   puts $reportFileId \n$t1\n

   foreach e [ memDetails ] {

       puts $reportFileId [ format "%-20s %s" " " $e ] 

   }

   puts  $reportFileId \n$t1
   puts  $reportFileId $t2
   puts  $reportFileId $t1
 
   emailReport $cpu

   ftruncate -fileid $reportFileId 0

}
######################################
# Proc - get memory details. 
######################################
proc memDetails {} {

   set width 18 
   array set meminfo [twapi::get_memory_info -all]

   catch { puts_tabular $width "Physical memory:" "Total [toMB $meminfo(-totalphysical)] MB, Available [toMB $meminfo(-availphysical)] MB" } r 
 
   set t1 $r

   catch { puts_tabular $width "Commit:"  "Total [toMB $meminfo(-totalcommit)] MB, Available [toMB $meminfo(-availcommit)] MB" } r 

   set t2 $r

   catch { puts_tabular $width "Swap files:" "[join $meminfo(-swapfiles) {, }]" } r

   set t3 $r

   return [ list $t1 $t2 $t3 ]

}
######################################
# Proc - get cpu details. 
######################################
proc processDetails {} {

   set processList [ lsort [ winutils::processes ] ]

   # calculate the cpu utilization for each process then sort and select the top ten. 
   
   foreach e $processList {

      set c [ twapi::get_process_info [ lindex $e 1 ] -processorutilization ] 

      lappend usageList [ list $e [ expr { int([ lindex $c 1 ]) } ] ]

   }

   set topTen [ lrange [ lsort -decreasing -integer -index 1 $usageList ] 0 9 ] 
  
   return $topTen

}

###########################################
# Email Report 
###########################################

proc emailReport { cpu } {

   global reportFile
   global reportFileId

   flush $reportFileId  

   set computerName $::env(COMPUTERNAME)

   if { [ expr { int($cpu) }  ] < 90 } { 

       set subject "$computerName - Cpu Alert Over."   

   } else {

       set subject "$computerName - Cpu Alert."   

   }

   sendSimpleMessage you@emailaddress.com $subject $reportFile

}
######################################
# Control Section.
######################################

######################################
# Set Variables
######################################

set processId [ twapi::get_current_process_id ]

set eventId   [ twapi::eventlog_open -write ]

set data "CHECKCPU STARTING"

twapi::eventlog_write $eventId 1 -type information -loguser -data $data

twapi::eventlog_close $eventId

set reportFile   [ file join $drive reports/notify/checkCpu.txt ]

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

checkCpu 
