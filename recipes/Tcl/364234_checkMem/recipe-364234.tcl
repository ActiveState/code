###########################################################
# Check physical memory usage. 
# Email alert if ram usage exceeds 90%.
# Display the top ten processes by memory usage.
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
package require math::fuzzy

######################################
# Proc - check memory usage. 
######################################
proc checkMem {} {

   puts "\n checkMem \n"

   while {1} { 

      # pause for 30 seconds 

      after 30000

      # check physical memory utilization over a ten second interval.
       
      array set meminfo [twapi::get_memory_info -all]

      set totalPhysicalMem $meminfo(-totalphysical)
      set availPhysicalMem $meminfo(-availphysical)
      set totalCommit      $meminfo(-totalcommit)
      set availCommit      $meminfo(-availcommit)
      set swapFiles        $meminfo(-swapfiles)

      set physicalMemUsage [ expr { (double ($totalPhysicalMem - $availPhysicalMem)/$totalPhysicalMem  ) } ] 
      
      set usedPerc [ expr { [math::fuzzy::troundn $physicalMemUsage 2] *100 } ]

#      if memory usage is > 90% and alert has not been generated send error report.

      if { ![ info exist report ] } { 
         
         set report false
         
      }
         
      if { $usedPerc > 90 && [ string is false $report ] } { 

	  set report true
          
          writeReport meminfo $usedPerc

      } else {

	  set continue true 

      }

      # if memory usage is < 90% and alert has been generated send OK report.

      if { $usedPerc < 90 && [ string is true $report ] } { 

	  set report false

          writeReport meminfo $usedPerc

      } else {

	  set continue true 

      }

   }

}
######################################
# Proc - write report
######################################
proc writeReport { meminfo usedPerc } {
  
   global reportFile
   global reportFileId

   upvar $meminfo a

   set header       "$::env(COMPUTERNAME) - Check Memory Usage"

   reportHeader $reportFileId $header $reportFile
 
   set s "*****************************************"
   set t1 [ format "%-15s %s" " " $s ]
   set s "The End"
   set t2 [ format "%-35s    %s" " " $s ]
   set t3 "$::env(COMPUTERNAME) -  Memory utilization is $usedPerc\%\. " 

   puts $reportFileId \n$t3\n

   set s "*****************************************"
   set t1 [ format "%-15s %s" " " $s ]

   foreach e [ memDetails a ] {

       puts $reportFileId [ format "%-15s %s" " " $e ] 

   }

   set t9 "Memory utilization - Top Ten" 

   puts $reportFileId \n$t1
   puts $reportFileId [ format "%-15s %s" " " $t9 ]
   puts $reportFileId $t1\n

   set spaces " "

   set w1 [ string length "ProcessName" ]
   set w2 [ string length "ProcessId"   ]
   set w3 [ string length "WorkingSet"  ]
   set w4 [ string length "WorkingsetPeak" ]

   puts $reportFileId [ format "%-15s %-20s %${w2}s %${w3}s %${w4}s\n" $spaces \
                                                             "ProcessName"   \
                                                             "ProcessId"     \
                                                             "WorkingSet"    \
                                                             "WorkingsetPeak"  ]

   foreach e [ processDetails ] {

      set processName    [ lindex $e 0 ]
      set processId      [ lindex $e 1 ]
      set workingset     [ toMB [ lindex $e 2 ] ]
      set workingsetpeak [ toMB [ lindex $e 3 ] ]

      set width [ string length $processId ]
                                              
      puts $reportFileId [ format "%-15s %-20s %${w2}s %${w3}s %${w4}s" $spaces \
                                                             $processName       \
                                                             "$processId"       \
                                                             "$workingset mb"   \
                                                             "$workingsetpeak mb" ]

   }

   puts  $reportFileId \n$t1
   puts  $reportFileId $t2
   puts  $reportFileId $t1

   emailReport $usedPerc

   ftruncate -fileid $reportFileId 0

}
######################################
# Proc - get memory details. 
######################################
proc memDetails { meminfo } {

   upvar $meminfo a

   set totalPhysicalMem $a(-totalphysical)
   set availPhysicalMem $a(-availphysical)
   set totalCommit      $a(-totalcommit)
   set availCommit      $a(-availcommit)
   set swapFiles        $a(-swapfiles)

   set width 30 

   catch { puts_tabular $width "Physical memory:" "Total [toMB $a(-totalphysical)] MB, Available [toMB $a(-availphysical)] MB" } r 
 
   set t1 $r

   catch { puts_tabular $width "Commit:"  "Total [toMB $a(-totalcommit)] MB, Available [toMB $a(-availcommit)] MB" } r 

   set t2 $r

   catch { puts_tabular $width "Swap files:" "[join $a(-swapfiles) {, }]" } r

   set t3 $r

   # allocated swap file space = (total commit memory - total physical memory)

   set swapFileSpace [ expr { $totalCommit - $totalPhysicalMem } ] 
 
   catch { puts_tabular $width "Allocated swap file space:" "[toMB $swapFileSpace] MB" } r 
   set t4 $r
   
   # available swap file space = (available commit memory - available physical memory)  
   
   set availSwapFileSpace [ expr { $availCommit - $availPhysicalMem } ]

   catch { puts_tabular $width "Available swap file space:" "[toMB $availSwapFileSpace] MB" } r 

   set t5 $r

   return [ list $t1 $t2 $t3 $t4 $t5 ]

}
##################################################
# Proc - get memory usage by top ten processes.
##################################################
proc processDetails {} {

#   puts "\n processDetails \n"

   set processList [ lsort [ winutils::processes ] ]

   # calculate the cpu utilization for each process then sort and select the top ten. 
   
   foreach e $processList {

      set processName [ lindex $e 0 ] 
      set processId   [ lindex $e 1 ] 

      array set meminfo [ twapi::get_process_info $processId -workingset -workingsetpeak]

      lappend usageList [ list $processName $processId $meminfo(-workingset) $meminfo(-workingsetpeak) ] 

   }

   set x      [ lsort -decreasing -integer -index 2 $usageList ]

   set topTen [ lrange [ lsort -decreasing -integer -index 2 $usageList ] 0 9 ] 
  
   return $topTen

}
###########################################
# Email Report 
###########################################

proc emailReport { usedPerc } {

   global reportFile
   global reportFileId

   flush $reportFileId  

   set computerName $::env(COMPUTERNAME)

   if { $usedPerc  < 90 } { 

       set subject "$computerName - Memory Alert Over."   

   } else {

       set subject "$computerName - Memory Alert."   

   }

   sendSimpleMessage you@youremail.com $subject $reportFile

}
######################################
# Control Section.
######################################

######################################
# Set Variables
######################################

set processId [ twapi::get_current_process_id ]

set eventId   [ twapi::eventlog_open -write ]

set data "CHECKMEM STARTING"

twapi::eventlog_write $eventId 1 -type information -loguser -data $data

twapi::eventlog_close $eventId

set reportFile   [ file join $drive reports/notify/checkMem.txt ]

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

checkMem 
