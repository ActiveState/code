# Recursive file compare utility for Windows.
# Calls diff.exe or fc.exe for each file found.

# Updated by John Brearley  Apr 2017
# email: brearley@bell.net
# email: jrbrearley4@gmail.com

# License: This script is free to use, modify and/or redistribute,
# however you MUST leave the author credit information above as is
# and intact.

# Support: Available on a best effort basis.

# Notes
# 1) For Win10, when you reboot with Repair disk, you cant run TCL from the command prompt.
#    There is something about the Repair DOS environment that does not let even a command line
#    oriented program to run. Same goes for Windows Powershell.
# 2) Need to try on Win7 Repair disk some time...
# 3) Some files are locked, so cant be read, eg c:\Windows\ServiceProfiles\LocalService\NTUSER.DAT
#    and FC gives misleading error about "no such file", even though it is visible.
# 4) regedit.exe is a perennial failure, but manually compares OK with fc.exe.
# 5) Upgrading TCL from 8.63b (Nov 2012) to 8.6.4.1 (Jan 2017) really reduced the number of errors
#    flagged, as the fc.exe retry mechanism shows many files are identical, even if diff.exe does
#    NOT agree. This is the fcr counter counter in the stats summary.


#==================== check_file_name ==================================
# Check if file is a constantly changing Windows or Norton file. These
# files are often locked down from even admin access, and cant be readily
# updated.
#
# Returns: "windows" | "norton" | "other"
#=======================================================================
proc check_file_name {file} {

   # NB: The categories used here MUST be kept in sync with ::cat_list !!!

   # Look for selected Windows or Norton directories.
   # NB: Some of the regexp patterns here rely on having the full file pathname!
   if {[regexp -nocase {^[a-z]:/?(ProgramData|Program\s*Files).*(Microsoft|Windows)} $file]} {
      return "windows"
   } elseif {[regexp -nocase {^[a-z]:/?(Windows|Users.*(Microsoft|Windows))} $file]} {
      return "windows"
   } elseif {[regexp -nocase {(hiberfil|pagefile|swapfile).*sys$} $file]} {
      return "windows"

   } elseif {[regexp -nocase {^[a-z]:/?(ProgramData|Program\s*Files).*Norton} $file]} {
      return "norton"
   } elseif {[regexp -nocase {^[a-z]:/?Users.*/Norton} $file]} {
      return "norton"

   } else {
      # Catchall for everything else.
      return "other"
   }
}


#==================== cleanup ==========================================
# Cleanup exit routine
#=======================================================================
proc cleanup { } {

   # log summary details
   set total_min [expr int(([clock seconds] - $::start_sec)/60)]
   log_info "\n[timestamp] $::self All done, $::error_cnt errors, $::nolog_cnt nolog, $::warning_cnt warn\
      \npattern=$::pattern src_dir=$::src_dir dest_dir=$::dest_dir"

   # Dump formatted stats names as header lines for a table.
   set f1 "%8s" ;# format for category column
   set f2 "%6s" ;# format for stat number column
   set hdr1 [format $f1 "category"]
   set hdr2 [format $f1 "========"]
   foreach i $::stat_list {
      # puts "i=$i"
      set hdr1 "$hdr1 [format $f2 $i]"
      set hdr2 "$hdr2 ======"
   }
   log_info "\n$hdr1\n$hdr2"

   # Dump formatted stats on table with one row per category.
   foreach i $::cat_list {
      set line [format $f1 $i] ;# start line with category name
      foreach j $::stat_list {
         set x $::stats_array($i,$j)
         set line "$line [format $f2 $x]"
         # puts "i=$i j=$j x=$x"
      }
      if {$i == "total"} {
         # Put visual break before total line.
         log_info $hdr2
      }
      log_info $line
   }

   # Other info
   log_info "\n$::subdir_cnt subdirectories, $::hidden_files_cnt hidden_files, $::hidden_subdir_cnt hidden_subdir, copy_opt=$::copy_opt"
   log_info "$::curly_tot_cnt curly_brace_tot, $::curly_matched_pair_cnt matched, $::curly_open_only_cnt open, $::curly_close_only_cnt close, $::curly_error_cnt error"
   log_info "TCL $::tcl_patchLevel, total time $total_min minutes \nsee $::out_file \nsee $::retry_file"

   # Exit with error count.
   exit $::error_cnt
}


#==================== compare_files ====================================
# Compares a specified source file to specified destination file
#
# Returns: OK, FAIL
#=======================================================================
proc compare_files {i src dest no_log category} {

   # If necessary, convert / to \ for optional retry by fc.exe
   set src2 $src
   set dest2 $dest
   # set ::compare_tool "fc.exe" ;# test code
   # First we escape curly-braces
   # if {[regexp {\{.*\}} $src]} {
   #    regsub -all "\{" $src2 "\\\{" src2 ;# Yes, 3 escapes, not 4!
   #    regsub -all "\}" $src2 "\\\}" src2 ;# Yes, 3 escapes, not 4!
   #    regsub -all "\{" $dest2 "\\\{" dest2 ;# Yes, 3 escapes, not 4!
   #    regsub -all "\}" $dest2 "\\\}" dest2 ;# Yes, 3 escapes, not 4!
   # }

   # Now covert / to \ Windows style.
   regsub -all {/} $src2  {\\} src2
   regsub -all {/} $dest2 {\\} dest2

   # Finally, add double-quotes for case of embedded whitespace.
   # No, this makes things worse...
   # if {[regexp {\s} $src2]} {
   #    set src2  "\"$src2\""
   #    set dest2 "\"$dest2\""
   # }
   # log_info "compare_files i=$i src2=$src2 dest2=$dest2"
   
   # Compare the files.
   if {$::compare_tool == "fc.exe"} {
      # fc.exe uses src2 / dest2 with windows path format
      set catch_resp [catch "exec $::compare_tool {$src2} {$dest2}" catch_msg]
   } else {
      # diff.exe uses Unix path format
      set catch_resp [catch "exec $::compare_tool {$src} {$dest}" catch_msg]
   }

   # If files compared OK, we are done.
   # set catch_resp 1 ;# test code
   if {$catch_resp == 0} {
      log_info "compare_files i=$i $dest $::compare_tool compared (OK)" "true"
      return "OK"
   }

   # For Windows & Program directories, compare again using fc.exe.
   # Tried wrapping fc.exe inside .bat file, also run as cmd.exe /c fc.bat, no improvement.
   set no_log [string trim $no_log]
   if {$::compare_tool != "fc.exe" && [regexp -nocase {^[a-z]:/?(Windows|Program)} $src]} {
      # See if fc.exe gives a different result.
      log_info "compare_file retry with fc.exe i=$i src2=$src2 dest2=$dest2 compare_tool=$::compare_tool no_log=$no_log"
      set catch_resp [catch "exec fc.exe {$src2} {$dest2}" catch_msg]
      set catch_msg [truncate_msg $catch_msg] ;# limit the garbage dumped into the log file
      log_info "fc.exe i=$i catch_resp=$catch_resp catch_msg=$catch_msg"
      # set catch_resp 0 ;# test code
      if {$catch_resp == 0} {
         # Always show when fc retry succeeded, increment specific counters for this event.
         log_info "compare_files i=$i $dest2 fc.exe retry compared (OK)"
         incr ::stats_array(total,fcr)
         incr ::stats_array($category,fcr)
         return "OK"
      }
   }

   # Deal with the error. The calling routine will suppress the first compare failure.
   set status [get_status $catch_msg $no_log $category "diff"]
   log_error "compare_files i=$i $dest $::compare_tool failed ($status $category)" $no_log
   # log_info "$catch_msg" ;# shows actual file differences, really floods the log.

   # Add this file to running list in DOS batch file for manual retry later on.
   log_retry $i $src $dest $no_log
   return "FAIL"
}


#==================== copy_file ========================================
# Copies specified source file to specified destination
#
# Returns: OK, FAIL
#=======================================================================
proc copy_file {i src dest dest_dir no_log category} {

   # If copy not requested, return.
   if {$::copy_opt == ""} {
      # Return status FAIL signals the calling routine to move on.
      # There are no stats counters to increment here.
      return "FAIL"
   }

   # If necessary, create the required destination directory.
   # TCL dirname has issue with unmatched close curly-brace, so we use the dest_dir 
   # that was passed to this routine
   # log_info "copy_file i=$i src=$src dest=$dest dest_dir=$dest_dir"
   if {![file isdirectory "$dest_dir"]} {
      set catch_resp [catch "file mkdir {$dest_dir}" catch_msg]
      # set catch_resp 1 ;# test code
      # set catch_msg abcd ;# test code
      if {$catch_resp == 0} {
         # Always log directory creation.
         log_info "copy_file i=$i created destination directory: $dest_dir (OK $category)" 
      } else {
         # Always log the error.
         set status [get_status $catch_msg "" $category]
         log_error "copy_file i=$i could not create dest_dir=$dest_dir, $catch_msg ($status $category)"
         # Increment the appropiate counters.
         incr ::stats_array(total,cpyfl)
         incr ::stats_array($category,cpyfl)
         return "FAIL"
      }

   } else {
      # puts "copy_file i=$i dest_dir=$dest_dir already exists, (OK $category)"
   }

   # Check if the source file is still there. There are a number of temporary folders,
   # such as /Windows/SoftwareDistribution/Download, also some Norton folders, where
   # items may have been found earlier by rec_find, but the OS has quietly purged
   # them by the time we actually get around to checking on them. 
   if {[file exists "$src"]} {
      # puts "copy_file i=$i src=$src still exists, (OK $category)"
   } else {
      # Always log the error.
      log_error "copy_file i=$i src=$src is now missing, (gone $category)"
      incr ::stats_array(total,gone)
      incr ::stats_array($category,gone)
      return "FAIL"
   }

   # Copy the file. File names have largely been vetted for unmatched curly-braces.
   set catch_resp [catch "file copy -force {$src} {$dest}" catch_msg]
   # set catch_resp 1 ;# test code
   # set catch_msg abcd ;# test code
   if {$catch_resp == 0} {
      log_info "copy_file i=$i copied $dest (OK $category)" $no_log
      return "OK"

   } else {
      # Always log the error.
      set status [get_status $catch_msg "" $category]
      log_error "copy_file i=$i could not copy to $dest, $catch_msg ($status $category)"
      incr ::stats_array(total,cpyfl)
      incr ::stats_array($category,cpyfl)
      return "FAIL"
   }
}


#==================== fix_curly ========================================
# Attempts to work around known issues with missing curly brackets in
# path/file names
#
# Returns: string
#=======================================================================
proc fix_curly {path category} {

   # NB: Initially, I had been converting / in pathnames to \ for the benefit
   # of fc.exe. This appears to have created a lot of issues with TCL file copy.
   # When the pathname looked like abc\def\\{1234}..., the open curly-brace looked
   # like it was being escaped, when in reality it was a directory delimiter.

   # NB: extra \ in pathname above is to work around TCL interpreter known issue of
   # unmatched curly braces in comments inside a loop, yes comments inside a loop,
   # choking up!!!

   # Deal with single unmatched curly-brace. This does NOT handle case of a 
   # correctly matched pair of curly-braces followed by an unmatched curly-brace.
   if {[regexp {(\{.*)} $path - x]} {
      # Found open curly-brace
      incr ::curly_tot_cnt
      # log_info "main i=$i file=$file found open curly-brace x=$x"
      # Check for matching close curly-brace AFTER the open curly-brace.
      # This is done by checking $x, which starts with the open curly-brace.
      if {[regexp {\}} $x]} {
         # TCL file copy works with matched curly-braces in the filenames, no need to escape them.
         incr ::curly_matched_pair_cnt
         # log_info "fix_curly found matched pair curly-braces x=$x path=$path category=$category"
      } else {
         incr ::curly_open_only_cnt
         regsub -all "\{" $path "\\\{" path ;# Yes, 3 escapes, not 4!
         # log_info "fix_curly escaped unmatched open curly-brace path=$path category=$category"
      }

   } elseif {[regexp {\}} $path]} {
      # There is no open curly-brace, but we found an unmatched close curly-brace
      incr ::curly_tot_cnt
      incr ::curly_close_only_cnt
      regsub -all "\}" $path "\\\}" path ;# Yes, 3 escapes, not 4!
      # log_info "fix_curly escaped unmatched close curly-brace path=$path category=$category"
   }

   # Return modified path
   return $path
}


#==================== get_status =======================================
# Parses the error msg, determines the appropriate status code and
# increments the appropriate category counter.
#
# Returns: string
#=======================================================================
proc get_status {msg no_log category {tool ""}} {

   # Look for selected error messages.
   set status ""
   set no_log [string trim $no_log]
   set tool [string trim $tool]
   # For tool=diff, use different counters.
   if {$tool == "diff"} {
      set status "diff"
      if {$no_log == ""} {
         incr ::stats_array(total,diff)
         incr ::stats_array($category,diff)
      }

   } elseif {[regexp -nocase "permission.*denied" $msg]} {
      set status "noacc"
      if {$no_log == ""} {
         incr ::stats_array($category,noacc)
         incr ::stats_array(total,noacc)
      }

   } elseif {[regexp -nocase "brace" $msg]} {
      set status "curly"
      if {$no_log == ""} {
         incr ::curly_error_cnt
         incr ::stats_array($category,curly)
         incr ::stats_array(total,curly)
      }

   } else {
      # Catch all bucket. 
      set status "unexp"
      if {$no_log == ""} {
         incr ::stats_array($category,unexp)
         incr ::stats_array(total,unexp)
      }
   }
   return $status
}


#==================== log_error ========================================
# Displays error message right now, adds message to the log file,
# increments error counter.
#
# Optional no_log parameter can suppress messages in log_file. This
# allows you to stop flooding the log_file for known conditions.
#=======================================================================
proc log_error {msg {no_log ""}} {

   # Prepend ERROR: & hand off to log_info
   set msg "ERROR: $msg"
   set no_log [string trim $no_log]
   if {$no_log == ""} {
      incr ::error_cnt
   }
   log_info $msg $no_log

   # Test code
   # if {$::error_cnt >= 100} {
   #    puts "\n\nToo many errors, stopping!"
   #    cleanup
   # }
}


#==================== log_info =========================================
# Displays info message right now, adds message to the log file.
#
# Optional no_log parameter can suppress messages in log_file. This
# allows you to stop flooding the log_file for known conditions.
#=======================================================================
proc log_info {msg {no_log ""}} {

   # Always display msg. Add "not logged" as appropriate.
   set no_log [string trim $no_log]
   if {$no_log != ""} {
      set msg "$msg (NL)"
      incr ::nolog_cnt
   }
   puts "$msg"

   # Append msg to running log file, when it is available for use.
   # no_log allows for suppressing repeated messages that flood the
   # log_file and make it unreadable.
   if {$::out != "" && $no_log == ""} {
      puts $::out "$msg"
      flush $::out
   }
}


#==================== log_retry ========================================
# Appends data to retry_cfc.bat file so user can easily manually retry
# failed file compare operations.
#=======================================================================
proc log_retry {i src dest no_log} {

   # For no_log not null, we are done
   set no_log [string trim $no_log]
   if {$no_log != ""} {
      return
   }

   # Now covert / to \ Windows style.
   regsub -all {/} $src  {\\} src
   regsub -all {/} $dest {\\} dest

   # Add this file to running list in DOS batch file for manual retry later on.
   puts $::retry "echo i=$i $src"
   puts $::retry "fc.exe \"$src\" \"$dest\""
   puts $::retry "echo i=$i $src"
   puts $::retry "if '%tr%' == '1' pause"
   flush $::retry
}

#==================== log_warning ======================================
# Appends specified WARNING msg to log file, displays msg on terminal.
#
# Optional no_log parameter can suppress messages in log_file. This
# allows you to stop flooding the log_file for known conditions.
#=======================================================================
proc log_warning {msg {no_log ""}} {

   # Prepend WARNING: & handoff to log_info
   set msg "WARNING: $msg"
   set no_log [string trim $no_log]
   if {$no_log == ""} {
      incr ::warning_cnt
   }
   log_info $msg $no_log
}


#==================== rec_find =========================================
# Takes list of file in the specified directory and adds them to the 
# global file list. Calls itself recursively for any subdirectories found.
#=======================================================================
proc rec_find {cur_dir} {

   # If no directories specified, we are done.
   set cur_dir [string trim $cur_dir]
   # puts "rec_find start cur_dir=$cur_dir"
   if {$cur_dir == ""} {
      return
   }

   # More recent versions of TCL 8.6+ seem to need a trailing / on the directories.
   # If not, rec_find will mess up and only get the subdirectories of pwd.
   # Also need trailing / for case of whole mounted subdirectory.
   # The setup routine ensures a single trailing / is present.

   # Get the category for this directory.
   set category [check_file_name $cur_dir]
   # puts "rec_find start cur_dir=$cur_dir category=$category"

   # Attempt to fix up known curly brace issues.
   # It turns out that glob cant handle directory name with unmatched curly brace either.
   # We allow the error to occur in order to make it more visible to the user.
   # So any files in a directory with unmatched curly braces are NOT listed and processed.
   # set cur_dir [fix_curly $cur_dir $category] ;# turned off so errors are NOT hidden!!!

   # Find all files in the current directory that match the specified pattern.
   # NB: You need to explicitly ask for hidden files as a separate glob request!
   # NB: Some directories start with $ (eg: $Recycle.Bin) which can make the TCL
   #     interpreter think this is a variable. So put { } around $cur_dir to fix.
   set current_files ""
   set status ""
   # log_info "rec_find(1) calling glob cur_dir=$cur_dir"
   set catch_resp [catch "set current_files \[glob -nocomplain -type f -directory {$cur_dir} $::pattern\]" catch_msg]
   # log_info "rec_find(1) return glob cur_dir=$cur_dir catch_resp=$catch_resp catch_msg=$catch_msg category=$category"
   if {$catch_resp != 0} {
      set  status [get_status $catch_msg "" $category]
      log_error "rec_find(1) $cur_dir $catch_msg ($status $category)"
   }
   set cnt_cf [llength $current_files]

   # Testing has shown that when you cant access a directory list of files due to
   # permission access issues or curly brace issues, you wont be able to get hidden file 
   # or directories either. So there is no point continuing onwards, getting the same 
   # error repeatedly.
   if {$status == "noacc" || $status == "curly"} {
      return
   }

   # Now get hidden files
   set hidden_files ""
   set catch_resp [catch "set hidden_files  \[glob -nocomplain -type {f hidden} -directory {$cur_dir} $::pattern\]" catch_msg]
   if {$catch_resp != 0} {
      set  status [get_status $catch_msg "" $category]
      log_error "rec_find(2) $cur_dir $catch_msg ($status $category)"
   }
   set cnt_hf [llength $hidden_files]
   incr ::hidden_files_cnt $cnt_hf
   # if {$hidden_files != ""} {
   #    log_info "\nrec_find cur_dir=$cur_dir \ncnt=$cnt_cf current_files=$current_files \ncnt=$cnt_hf hidden_files=$hidden_files"
   # }

   # Get sorted unique list of all files
   set sorted_files [lsort -unique "$current_files $hidden_files"]
   set cnt_sf [llength $sorted_files]
   # log_info "rec_find cur_dir=$cur_dir cnt_sf=$cnt_sf"

   # Save each file as a seperate element in file_array. This avoids issues
   # with long lists and mismatched curly braces for filenames that have
   # embedded spaces or curly braces in them
   foreach file $sorted_files {
      set cnt_tot $::stats_array(total,found)
      incr cnt_tot
      set ::stats_array(total,found) $cnt_tot
      set ::file_array($cnt_tot) $file ;# NB: This is the full file pathname!
      if {$cnt_tot % 1000 == 0} {
         log_info "rec_find i=$cnt_tot file=$file ($category)" "true"
      }
      # log_info "rec_find i=$cnt_tot file=$file ($category)" "true"
      set category [check_file_name $file]
      incr ::stats_array($category,found)
   }

   # Find all subdirectories at this level. 
   set current_subdir ""
   set catch_resp [catch "set current_subdir \[glob -nocomplain -type d -directory {$cur_dir} *\]" catch_msg]
   if {$catch_resp != 0} {
      set  status [get_status $catch_msg "" $category]
      log_error "rec_find(3) $cur_dir $catch_msg ($status $category)"
   }
   set cnt_csd [llength $current_subdir]

   # You need to explicitly ask for hidden directories
   set hidden_subdir ""
   set catch_resp [catch "set hidden_subdir \[glob -nocomplain -type {d hidden} -directory {$cur_dir} *\]" catch_msg]
   if {$catch_resp != 0} {
      set  status [get_status $catch_msg "" $category]
      log_error "rec_find(4) $cur_dir $catch_msg ($status $category)"
   }
   set cnt_hsd [llength $hidden_subdir]
   incr ::hidden_subdir_cnt $cnt_hsd
   # if {$hidden_subdir != ""} {
   #    log_info "\nrec_find cur_dir=$cur_dir \ncnt=$cnt_csd current_subdir=$current_subdir \ncnt=$cnt_hsd hidden_subdir=$hidden_subdir"
   # }

   # Get sorted unique list of all subdirectories
   set sorted_subdir [lsort -unique "$current_subdir $hidden_subdir"]
   set cnt_ssd [llength $sorted_subdir]
   # log_info "rec_find cur_dir=$cur_dir cnt_ssd=$cnt_ssd"

   # Call ourselves recursively for each subdirectory.
   foreach dir $sorted_subdir {
      incr ::subdir_cnt
      # puts "calling rec_find cur_dir=$cur_dir next subdir dir=$dir"
      rec_find "$dir"
   }
}


#==================== setup ============================================
# Does basic initialization, gives online help if needed.
#=======================================================================
proc setup { } {

   # Initialize global counters
   set ::curly_close_only_cnt 0
   set ::curly_error_cnt 0
   set ::curly_matched_pair_cnt 0
   set ::curly_open_only_cnt 0
   set ::curly_tot_cnt 0
   set ::copy_opt "" ;# null value used to control optional logging of events.
   set ::error_cnt 0
   set ::hidden_files_cnt 0
   set ::hidden_subdir_cnt 0
   set ::nolog_cnt 0
   set ::out "" ;# log file is not available yet
   set ::subdir_cnt 0
   set ::warning_cnt 0

   # Set up global stats array, indexed by category & statistic name.
   # NB: The order of the items in these lists determines the data table 
   # order of the rows and columns displayed by the exit cleanup routine.
   set ::cat_list "windows norton other total"
   set ::stat_list "noacc found miss diff repr cpyfl gone curly unexp fcr"
   foreach i $::cat_list {
      foreach j $::stat_list {
         set ::stats_array($i,$j) 0
         set x $::stats_array($i,$j)
         # puts "stats_array i=$i j=$j x=$x"
      }
   }

   # Give online help if necessary
   set ::self [file tail $::argv0]
   set x [lindex $::argv 0]
   set x [string tolower $x]
   set x [string range $x 0 1]
   if {$x == "-h" || $x == "/?"} {
      puts "Basic Usage: tclsh $::self \[pattern\] \[src_dir\] \[dest_dir\] <-copy>"
      puts " "
      puts "Utility recursively gets list of all files in the src_dir"
      puts "directory that match the specified \[pattern\]. Files are compared" 
      puts "to same file name in the \[dest_dir\] using diff.exe or fc.exe."
      puts " "
      puts "Use pattern \"*\" to compare all files."
      puts "Use pattern \"*.jpeg\" to compare only .jpg files."
      puts " " 
      puts "Optional <-copy> will copy missing or overwrite different files in"
      puts "the \[destination_directory\]." 
      exit 1
   }

   # Save start time, in seconds.
   set ::start_sec [clock seconds]

   # Check for 3 required command line tokens
   if {$::argc < 3} {
      log_error "Must specify minimum 3 command line tokens! \nFor more info, type: tclsh $::self -h"
      exit 1
   }

   # Get 3 required command line parms.
   regsub -all {\\} $::argv {/} ::argv ;# convert \ for windows filesystem to / 
   set ::pattern [lindex $::argv 0]
   set ::src_dir [lindex $::argv 1]
   if {[regexp {^\.} $::src_dir]} {
      regsub {^\.} $::src_dir [pwd] ::src_dir ;# convert relative path to full path
   }
   set ::dest_dir [lindex $::argv 2]
   if {[regexp {^\.} $::dest_dir]} {
      regsub {^\.} $::dest_dir [pwd] ::dest_dir ;# convert relative path to full path
   }

   # More recent versions of TCL 8.6+ seem to need a single trailing / on the directories.
   # If not, rec_find calls to glob will mess up and only get the subdirectories of pwd.
   # Also need trailing / for case of whole mounted subdirectory.
   set ::src_dir "${::src_dir}/"
   set ::dest_dir "${::dest_dir}/"

   # Convert multiple repeated / in directories to a single /.
   # NB: The extra / royally messed up destination file path computations made in main program loop.
   #     The leading charactar of each directory got lost, causing each directory to be recopied with
   #     the wrong name, filled up the destination disk.
   # NB: For the case of temporary network mounts in the form of //host/directory, we MUST preserve 
   #     the leading //. This is why we start the regsub pattern matching after the first 2 characters!
   regsub -start 2 -all {/+} $::src_dir {/} ::src_dir
   regsub -start 2 -all {/+} $::dest_dir {/} ::dest_dir

   # Needed in main program loop for computing correct destination directory
   set ::src_dir_len [string length $::src_dir]

   # Check for optional -copy token.
   if {$::argc >= 4} {
      set y [lindex $::argv 3]
      set y [string tolower $y]
      if {$y == "-copy"} {
         set ::copy_opt "true"
      } else {
         log_error "Invalid option: $y ! \nFor more info, type: tclsh $::self -h"
         exit 1
      }
   }

   # Choose directory for log file & retry batch file based on known options of different OS.
   # NB: Windows admin user usually doesnt have HOMEPATH defined, but does have USERPROFILE.
   if {[info exists ::env(HOMEPATH)]} {
      set out_path $::env(HOMEPATH) ;# Windows first choice
   } elseif {[info exists ::env(USERPROFILE)]} {
      set out_path $::env(USERPROFILE) ;# Windows second choice, often needed by admin
   } elseif {[info exists ::env(HOME)]} { 
      set out_path $::env(HOME) ;# Linux default
   } else {
      set out_path "[pwd]"
   }
   regsub -all {\\} $out_path {/} out_path ;# convert \ for windows filesystem to /

   # Choose log file name.
   set log_fn [file root $::self]
   set ::out_file "$out_path/$log_fn.log"

   # Open running log file for append.
   set catch_resp [catch "set ::out \[open \"$::out_file\" a\]" catch_msg]
   if {$catch_resp != 0} {
      log_error "Could not open $::out_file catch_msg=$catch_msg"
      exit 1
   }
   # puts "out_path=$out_path out_file=$::out_file out=$::out"

   # Choose error retry DOS batch file name.
   set retry_fn "retry_fc"
   set ::retry_file "$out_path/$retry_fn.bat"

   # Open running error retry DOS batch file for append.
   set catch_resp [catch "set ::retry \[open \"$::retry_file\" a\]" catch_msg]
   if {$catch_resp != 0} {
      log_error "Could not open $::retry_file catch_msg=$catch_msg"
      exit 1
   }
   # puts "out_path=$out_path retry_file=$::retry_file retry=$::retry"

   # Log start date/time, calling parms.
   set ts [timestamp]
   log_info "\n$ts $::self starting pattern=$::pattern\
      \nsrc_dir=$::src_dir dest_dir=$::dest_dir copy_opt=$::copy_opt\
      \nsee: $::out_file \nsee$::retry_file"

   # Add header to retry DOS batch file.
   puts $::retry "\n\n@echo off\necho.\necho.\necho $ts issues from $::self"
   flush $::retry

   # Check source directory exists.
   if {![file isdirectory "$::src_dir"]} {
      log_error "src_dir=$::src_dir not found!"
      exit 1
   }

   # Check destination directory exists.
   if {![file isdirectory "$::dest_dir"]} {
      log_error "dest_dir=$::dest_dir not found!"
      exit 1
   }

   # Are src_dir & dest_dir the same? We allow this for self-test, but warn user.
   if {[string tolower $::src_dir] == [string tolower $::dest_dir]} {
      log_warning "$::self setup src_dir EQ dest_dir $::src_dir !"
      log_warning "Hopefully you are doing a self-test here?"
      log_warning "All files MUST be identical in this case!"
   }

   # Choose compare_tool. If tkdiff suite is not available, then use fc.exe.
   set ::compare_tool "diff.exe"
   set catch_resp [catch "exec $::compare_tool --help" catch_msg]
   if {$catch_resp == 0} {
      # diff.exe give rc=0 on help msg.
      log_info "$::compare_tool is present (OK)"
   } else {
      # Look at error msg. If diff.exe not found, switch to fc.exe.
      if {[regexp "couldn.t.*execute.*no.*such.*file" $catch_msg]} {
         log_info "$::compare_tool does not appear to be installed: $catch_msg"
         set ::compare_tool "fc.exe"
         log_warning "Default tool $::compare_tool is known to lockup on large runs"
      } else {
         log_error "$::compare_tool unexpected response: $catch_msg"
      }
   }
}


#==================== timestamp ========================================
# Returns current date & time formatted as: YYYY/MM/DD HH:MM
#=======================================================================
proc timestamp { } {

   return [clock format [clock seconds] -format "%Y/%m/%d %H:%M"]
}


#==================== truncate_msg =====================================
# Truncates a msg string to limit how much garbage gets dumped into the
# log file.
# 
# Returns: string
#=======================================================================
proc truncate_msg {msg} {

   # Define max length of msg to return.
   set max_len 300

   # Get length of msg.
   set len [string length $msg]

   # Do we need to truncate the msg?
   if {$len <= $max_len} {
      return $msg
   } else {
      set len $max_len
      set msg [string range $msg 0 $len]
      # log_info "truncate_msg len=$len msg=$msg"
      return $msg
   }
}


#==================== Main program =====================================
# Main program
#=======================================================================
# Initialization, give help if needed.
setup

# Test code
# log_info "copied file afdfsdf"
# log_info "should not be logged" "no_log"
# log_error "fsdf sf sf sf sd "
# log_error "error should not be logged" "no_log"
# log_warning "test warn"
# log_warning "warning should not be logged" "no_log"
# cleanup

# Recursively get all files that match the desired pattern.
rec_find "$src_dir"
log_info "[timestamp] main found $::stats_array(total,found) files, $subdir_cnt subdirectories,\
   $error_cnt errors, $::stats_array(total,noacc) noacc \nsee $out_file \nsee$::retry_file"

# Compare source file with corresponding file in destination_directory.
# When copy_opt=true, copy missing files, recopy different files and compare again.
for {set i 1} {$i <= $stats_array(total,found)} {incr i} {

   # Get the source file full path name & src_subdir.
   set src_path $file_array($i) ;# NB: file full source path name is in file_array!
   set src_subdir [file dirname "$src_path"]
   if {![regexp {/$} $src_subdir]} {
      set src_subdir "${src_subdir}/" ;# add trailing / if missing
   }
   set src_file [file tail $src_path]

   # Check if this file is one of the constantly changing Windows or Norton files.
   # This category is used to classify error messages with separate statistic counts,
   # resulting in a much more comprehensible log.
   set category [check_file_name $src_path]
   set category [string trim $category]

   # TCL dirname has issue with unmatched escaped close curly-brace, so save dest_subdir here
   # before we escape the curly-braces.
   # regsub messes up when directory names have embedded spaces
   # set dest_subdir ""
   # regsub "$src_dir" "$src_subdir" "$dest_dir" dest_subdir ;# doesnt always work!
   # puts "regsub: dest_subdir=$dest_subdir"

   # So we use string range to correctly get dest_subdir
   set dest_subdir [string range $src_subdir $src_dir_len end]
   set dest_subdir "${dest_dir}${dest_subdir}" ;# dont need to insert /
   
   # Set the destination file full path name.
   set dest_path "${dest_subdir}${src_file}" ;# dont need to insert /

   # Attempt to fix up known curly brace issues.
   set src_path [fix_curly $src_path $category]
   set dest_path [fix_curly $dest_path $category]
   # log_info "main i=$i src_path=$src_path src_subdir=$src_subdir src_file=$src_file \
   #    dest_subdir=$dest_subdir dest_path=$dest_path category=$category"

   # Watch for src_path EQ dest_path. Error vs Warning response depends on 
   # what user specified for src_dir & dest_dir. We keep processing this
   # file, regardless.
   # set dest_path $src_path ;# test code
   if {[string tolower $src_path] == [string tolower $dest_path]} {
      if {[string tolower $src_dir] == [string tolower $dest_dir]} {
         log_warning "main i=$i src_path EQ dest_path $src_path, src_dir EQ dest_dir $src_dir, presumably this is a self-test, all files MUST be identical!"
      } else {
         log_error "main i=$i src_path EQ dest_path $src_path, BUT src_dir=$src_dir NE dest_dir=$dest_dir, something went seriously wrong! (unexp $category)"
         incr stats_array(total,unexp)
         incr ::stats_array($category,unexp)
      }
   }

   # Check if destination file exists, copy if requested.
   set repair "no"
   if {[file exists "$dest_path"]} {
       log_info "main i=$i $dest_path found (OK $category)" "true"
   } else {
      log_error "main i=$i dest_path=$dest_path NOT found (missing $category)" $copy_opt
      # Always count missing files. These stats help explain what we really did.
      incr stats_array(total,miss)
      incr stats_array($category,miss)
      
      # If requested, copy the file. File copy success is NOT logged, as
      # we will keep processing this file. However, file copy error is always
      # logged, as this will be the last thing we do for this file.
      set rc [copy_file $i "$src_path" "$dest_path" "$dest_subdir" $copy_opt $category]
      if {$rc == "OK"} {
         # File was successfully copied.
         set repair "yes" ;# shows we are attempting to repair file
      } else {
         # If copy_opt was null, then we did NOT try to copy the file, and
         # we move on to the next file, perfectly normal occurance. 
         # If copy_opt was true, we tried and failed to copy this file. 
         # The copy error is logged, and we move on to the next file.
         continue
      }
   }

   # Compare src & dest files. The first compare error can be suppressed
   # when copy_opt is true.  
   set rc [compare_files $i "$src_path" "$dest_path" $copy_opt $category]
   if {$rc == "OK"} {
      # Are we trying to repair this file?
      if {$repair == "yes"} {
         # Repairs are complete. 
         incr stats_array(total,repr)
         incr stats_array($category,repr)
         log_info "main i=$i repair(1) succeeded $dest_path (OK $category)"
       }
       # Processing this file is all done.
       continue

   } else {
      # Files are different. Do we copy and compare again?
      if {$::copy_opt != ""} {
         set rc [copy_file $i "$src_path" "$dest_path" "$dest_subdir" $copy_opt $category]
         if {$rc != "OK"} {
            # We tried and failed to copy this file. Copy error will always be logged.
            # First compare failed, so add this file to running list in DOS batch file for manual retry later on.
            log_retry $i $src_path $dest_path ""
            continue
         }
         # One last try at comparing these files. At this point, we always log
         # the compare errors.
         set rc [compare_files $i "$src_path" "$dest_path" "" $category]
         if {$rc == "OK"} {
            incr stats_array(total,repr)
            incr stats_array($category,repr)
            log_info "main i=$i repair(2) succeeded $dest_path (OK $category)"
         }
      }
   }
}

# Cleanup routine
cleanup
