# Differential file copy utility for Windows.
# File is copied if it is not present in the destination folder
# or the existing destination copy has an older modified date/time
# stamp or it has the same date/time stamp but a different file size.
# There are options to show/remove older files from destination folder,
# also options to show what would be copied, but not actually copy.

# Updated by John Brearley  Apr 2017
# email: brearley@bell.net
# email: jrbrearley4@gmail.com

# License: This script is free to use, modify and/or redistribute,
# however you MUST leave the author credit information above as is
# and intact.

# Support: Available on a best effort basis.

# Should work on Linux, but has not been tested on Linux yet.


#==================== cleanup =========================================
# Cleanup routine, dumps stats.
#
# Exits the script.
#=======================================================================
proc cleanup {} {

   # Cleanup routine. Get script run time.
   set total_min [expr int(([clock seconds] - $::start_sec)/60)]

   # Log the primary stats.
   if {$::opt_copy == "-showcopy"} {
      set label1 "NOT"
   } else {
      set label1 ""
   }
   log_info "[timestamp] $::self All done, src_dir $::src_dir, dest_dir $::dest_dir,\
      total $::total_src_files source files found, $::total_src_subdir dir,\
      $label1 copied $::new_files new files, $label1 updated $::updated_files files,\
      deleted $::deleted files, showold $::showold files, $::errors errors, $::warnings warnings,\
      total time $total_min minutes, see log_file: $::out_file"

   # Log the secondary stats.
   log_info "misc: $::force_files forced copies, $::empty_dir_found empty dir found,\
      $::empty_dir_deleted empty dir deleted, $::empty_dir_kept empty dir kept,\
      $::total_src_hidden_files hidden files, $::total_src_hidden_subdir hidden dir,\
      $::curly_cnt curly err, $::fulldisk_cnt fulldisk err, $::noacc_cnt noacc err,\
      $::unexp_cnt unexp err"

   # Close the log file, exit the script.
   close $::out
   exit $::errors
}


#==================== get_status =======================================
# Parses the error msg, determines the appropriate status code and
# increments the appropriate category counter.
#
# Returns: string, exits script if too many fulldisk errors occur.
#=======================================================================
proc get_status {msg} {

   # Look for selected error messages.
   set status ""
   if {[regexp -nocase "permission.*denied" $msg]} {
      set status "noacc"
      incr ::noacc_cnt

   } elseif {[regexp -nocase "brace" $msg]} {
      set status "curly"
      incr ::curly_cnt

   } elseif {[regexp -nocase "no.*space.*left" $msg]} {
      set status "fulldisk"
      incr ::fulldisk_cnt
      if {$::fulldisk_cnt >= 50} {
         log_error "get_status Too many fulldisk errors occurred, stopping script, $msg ($status)"
         cleanup
      }

   } else {
      # Catch all bucket. 
      set status "unexp"
      incr ::unexp_cnt
   }
   return $status
}


#==================== log_error ========================================
# Appends specified ERROR msg to log file, displays msg on terminal.
#=======================================================================
proc log_error {msg} {

   # Prepend ERROR: & handoff to log_info
   set msg "ERROR: $msg"
   incr ::errors
   log_info $msg
}


#==================== log_info =========================================
# Appends specified msg to log file, displays msg on terminal.
#=======================================================================
proc log_info {msg} {

   # Append msg to running log file, when it is available for use.
   if {$::out != ""} {
      puts $::out "$msg"
      flush $::out
   }

   # Display msg on terminal.
   puts "$msg"
}


#==================== log_warning ======================================
# Appends specified WARNING msg to log file, displays msg on terminal.
#=======================================================================
proc log_warning {msg} {

   # Prepend WARNING: & handoff to log_info
   set msg "WARNING: $msg"
   incr ::warnings
   log_info $msg
}


#==================== rec_find =========================================
# Takes list of files in the specified directory and adds them to the 
# global file_array, along with modified date/time/size info. Calls 
# itself recursively for any subdirectories found.
#
# NB: This routine will operate on the source directory, or the
# destination directory, as needed, depending on the calling parameter.
#=======================================================================
proc rec_find {cur_dir} {

   # If no directory was specified, we are done.
   set cur_dir [string trim $cur_dir]
   if {$cur_dir == ""} {
      return
   }

   # More recent versions of TCL 8.6+ seem to need a trailing / on the directories.
   # If not, rec_find will mess up and only get the subdirectories of pwd.
   # Also need trailing / for case of whole mounted subdirectory.
   # The setup routine ensures a single trailing / is present.

   # It turns out that glob cant handle directory name with unmatched curly brace either.
   # We allow the error to occur in order to make it more visible to the user.
   # So any files in a directory with unmatched curly braces are NOT listed and processed.

   # Find all files in the current directory. 
   # NB: You need to explicitly ask for hidden files as a seperate glob request.
   # NB: Some directories start with $ (eg: $Recycle.Bin) which can make the TCL
   #     interpreter think this is a variable. Other files or directories can 
   #     have [text] which TCL thinks is a command. So put { } around $cur_dir to fix.
   set current_files ""
   set status ""
   set catch_resp [catch "set current_files \[glob -nocomplain -type f -directory {$cur_dir} *\]" catch_msg]
   # log_info "rec_find(1) return glob cur_dir=$cur_dir catch_resp=$catch_resp catch_msg=$catch_msg"
   if {$catch_resp != 0} {
      set status [get_status $catch_msg]
      log_error "rec_find(1) $cur_dir $catch_msg ($status)"
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
   set catch_resp [catch "set hidden_files \[glob -nocomplain -type {f hidden} -directory {$cur_dir} *\]" catch_msg]
   # log_info "rec_find(2) return glob cur_dir=$cur_dir catch_resp=$catch_resp catch_msg=$catch_msg"
   if {$catch_resp != 0} {
      set status [get_status $catch_msg]
      log_error "rec_find(2) $cur_dir $catch_msg ($status)"
   }
   set cnt_hf [llength $hidden_files]
   incr ::hidden_files_cnt $cnt_hf
   # if {$cnt_hf > 0} {
   #    log_info "rec_find hidden_files=$hidden_files"
   # }

   # Get sorted unique list of all files.
   set sorted_files [lsort -unique "$current_files $hidden_files"]
   set cnt_sf [llength $sorted_files]
   # log_info "rec_find cur_dir=$cur_dir cnt_sf=$cnt_sf current_files=$current_files hidden_files=$hidden_files cnt_hf=$cnt_hf"

   # Save each file as a seperate element in file_array. This avoids issues
   # with long lists and mismatched curly braces for filenames that have
   # embedded spaces in them. Also get the file modified date/time info.
   foreach file $sorted_files {
      incr ::total_files
      set ::file_array($::total_files,name) $file ;# NB: This is the full file pathname!
      if {$::total_files % 1000 == 0} {
         puts "rec_find i=$::total_files file=$file"
      }

      # Most of the time the file will exist in the other directory, so we
      # we always cache the modified date/time & size info for the file.
      # This modified date/time info will be extraneous only if the file is 
      # not in the other directory, or we are doing a -delete cleanup.
      set catch_resp [catch "set modified_sec \[file mtime {$file}\]" catch_msg]
      if {$catch_resp != 0} {
         set modified_sec 0
         set status [get_status $catch_msg]
         log_error "rec_find mtime $file $catch_msg ($status)"
      }

      # Create human readable date/time.
      # set modified_sec "abc" ;# test code
      set catch_resp [catch "set modified_date_time \[clock format $modified_sec -format \"%Y/%m/%d %H:%M:%S\"\]" catch_msg]
      if {$catch_resp != 0} {
         set modified_date_time "-/-/- -:-:-"
         set status [get_status $catch_msg]
         log_error "rec_find date/time $file $catch_msg ($status)"
      }

      # Now get file size, in bytes.
      set catch_resp [catch "set byte_size \[file size {$file}\]" catch_msg]
      if {$catch_resp != 0} {
         set byte_size -1
         set status [get_status $catch_msg]
         log_error "rec_find size $file $catch_msg ($status)"
      }

      # Save data in global file_array.
      # puts "rec_find i=$::total_files file=$file modified: $modified_sec sec, $modified_date_time, size: $byte_size bytes"
      set ::file_array($::total_files,modified_sec) $modified_sec
      set ::file_array($::total_files,modified_date_time) $modified_date_time
      set ::file_array($::total_files,byte_size) $byte_size
   }

   # Find all subdirectories at this level.
   set current_subdir ""
   set catch_resp [catch "set current_subdir \[glob -nocomplain -type d -directory {$cur_dir} *\]" catch_msg]
   # log_info "rec_find(3) return glob cur_dir=$cur_dir catch_resp=$catch_resp catch_msg=$catch_msg"
   if {$catch_resp != 0} {
      set status [get_status $catch_msg]
      log_error "rec_find(3) $cur_dir $catch_msg ($status)"
   }
   set cnt_csd [llength $current_subdir]

   # You need to explicitly ask for hidden directories
   set hidden_subdir ""
   set catch_resp [catch "set hidden_subdir \[glob -nocomplain -type {d hidden} -directory {$cur_dir} *\]" catch_msg]
   # log_info "rec_find(4) return glob cur_dir=$cur_dir catch_resp=$catch_resp catch_msg=$catch_msg"
   if {$catch_resp != 0} {
      set status [get_status $catch_msg]
      log_error "rec_find(4) $cur_dir $catch_msg ($status)"
   }
   set cnt_hsd [llength $hidden_subdir]
   incr ::hidden_subdir_cnt $cnt_hsd
   # log_info "rec_find cur_dir=$cur_dir \ncnt=$cnt_csd current_subdir=$current_subdir \ncnt=$cnt_hsd hidden_subdir=$hidden_subdir"
   
   # Get sorted unique list of all subdirectories
   set sorted_subdir [lsort -unique "$current_subdir $hidden_subdir"]
   set cnt_ssd [llength $sorted_subdir]
   # log_info "rec_find cur_dir=$cur_dir cnt_ssd=$cnt_ssd"

   # Check for empty directories, delete as appropriate.
   # NB: If there is a chain of nested empty subdirectories, it will take multiple runs of this
   # routine to clean them all out, as we only delete the bottom of the chain each run.
   if {$sorted_files == "" && $sorted_subdir == ""} {
      incr ::empty_dir_found
      if {$::opt_keep == "-keepempty"} {
         incr ::empty_dir_kept
         log_info "rec_find Would have deleted empty dir=$cur_dir, did NOT due to $::opt_keep"
      } else {
         # set t1 [open "$cur_dir/a.txt" a] ;# test code to create dummy file in supposedly empty directory
         # NB: DONT use -force option for file delete!
         # This acts as a final safety check that the directory REALLY is empty!
         set catch_resp [catch "file delete {$cur_dir}" catch_msg]
         # log_info "rec_find Delete empty dir=$cur_dir catch_resp=$catch_resp catch_msg=$catch_msg"
         if {$catch_resp == 0} {
            incr ::empty_dir_deleted
            log_info "rec_find Deleted empty dir=$cur_dir OK"
         } else {
            set status [get_status $catch_msg]
            log_error "rec_find Delete empty dir=$cur_dir $catch_msg ($status)"
         }
      }
   }

   # Call ourselves recursively for each subdirectory.
   foreach dir $sorted_subdir {
      incr ::subdir_cnt
      # log_info "calling rec_find cur_dir=$cur_dir next subdir dir=$dir"
      rec_find "$dir" ;# NB: This is the full directory pathname!
   }
}


#==================== Setup ============================================
# Does basic setup
#=======================================================================
proc setup { } {

   # Initialize stats counters
   set ::curly_cnt 0
   set ::deleted 0
   set ::fulldisk_cnt 0
   set ::empty_dir_deleted 0
   set ::empty_dir_found 0
   set ::empty_dir_kept 0
   set ::errors 0
   set ::force_files 0
   set ::hidden_files_cnt 0
   set ::hidden_subdir_cnt 0
   set ::new_files 0
   set ::noacc_cnt 0
   set ::out "" ;# log file is not available yet
   set ::showold 0
   set ::subdir_cnt 0
   set ::total_files 0
   set ::unexp_cnt 0
   set ::updated_files 0
   set ::warnings 0
   
   # Give online help if necessary
   set ::self [file tail $::argv0]
   set x [lindex $::argv 0]
   set x [string tolower $x]
   set x [string range $x 0 1]
   if {$x == "-h" || $x == "/?"} {
      puts "Usage: tclsh $::self source_directory destination_directory"
      puts "<-delete> <-force> <-keepempty> <-showcopy|-sc> <-showold|-so>"
      puts "<-trace>"
      puts " "
      puts "Utility recursively gets list of all files in source directory"
      puts "and checks the destination directory. The file is copied to the" 
      puts "destination directory only if it is not there or the existing" 
      puts "destination copy has an older date/time stamp, or different" 
      puts "file size byte count."
      puts " "
      puts "Wildcard parsing on options is done to minimize typing."
      puts " "
      puts "Option -delete will remove files in destination_directory that"
      puts "are NOT in the source_directory, taking out the old trash."
      puts " "
      puts "Option -force will copy files to the destination, regardless of"
      puts "destination file date/time stamps."
      puts " "
      puts "Option -keepempty will leave empty subdirectories in place. By default"
      puts "empty subdirectories will be deleted. If there is a chain of nested empty"
      puts "subdirectories, it will take multiple runs of this routine to clean them"
      puts "all out, as we only delete the bottom of the chain each run."
      puts " "
      puts "Options -showcopy -sc will simply SHOW the source files that WOULD be"
      puts "copied, but does NOT actually copy them. This lets you see what"
      puts "WOULD be copied, but NOT actually do the copies."
      puts " "
      puts "Options -showold -so will simply SHOW the files in destination_directory"
      puts "that are NOT in the source_directory, but does NOT remove them. This"
      puts "lets you see what the -delete option WOULD delete, but NOT actually do the"
      puts "deletions."
      puts " "
      puts "Option -trace adds 1 line of data per file processed showing what was used"
      puts "to make decisions about this file. This can flood the logfile, be careful!"
      exit 1
   }

   # Check for 2 command line tokens
   if {$::argc < 2} {
      log_error "setup You MUST specify 2 command line tokens minimum."
      log_info "\nFor more info, type: tclsh $::self -h"
      exit 1
   }

   # Save start time, in seconds.
   set ::start_sec [clock seconds]

   # Set command line parms
   regsub -all {\\} $::argv {/} ::argv ;# convert \ for windows filesystem to /
   # puts "argv: $::argv"
   set ::src_dir [lindex $::argv 0]
   if {[regexp {^\.} $::src_dir]} {
      regsub {^\.} $::src_dir [pwd] ::src_dir ;# convert relative path to full path
   }
   set ::dest_dir [lindex $::argv 1]
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

   # Needed in main program loop for computing correct destination directory.
   set ::src_dir_len [string length $::src_dir]
   set ::dest_dir_len [string length $::dest_dir]
   # puts "setup src_dir=$::src_dir src_dir_len=$::src_dir_len dest_dir=$::dest_dir dest_dir_len=$::dest_dir_len"

   # Parse remaining calling args, if any.
   # NB: Some options conflict with each other, last one wins.
   set opt_string [lrange $::argv 2 end]
   # puts "opt_string=$opt_string"
   set ::opt_cleanup ""
   set ::opt_copy ""
   set ::opt_keep ""
   set ::opt_trace ""
   foreach x $opt_string {
      # Get next option
      set x [string tolower $x]
      # puts "x=$x"

      # NB: -delete & -showold are mutually exclusive options!

      # Look for wildcard match -delete option
      if {[regexp {^\-+d} $x]} {
         if {$::opt_cleanup != ""} {
            log_warning "setup ignoring previous option $::opt_cleanup, using $x"
         } 
         set ::opt_cleanup "-delete"
         continue
      }

      # Look for wildcard match -showold option
      if {[regexp {^\-+sh?o?w?o} $x]} {
         if {$::opt_cleanup != ""} {
            log_warning "setup ignoring previous option $::opt_cleanup, using $x"
         } 
         set ::opt_cleanup "-showold"
         continue
      }

      # NB: -force & -showcopy are mutually exclusive options!

      # Look for wildcard match -force option
      if {[regexp {^\-+f} $x]} {
         if {$::opt_copy != ""} {
            log_warning "setup ignoring previous option $::opt_copy, using $x"
         } 
         set ::opt_copy "-force"
         continue
      }

      # Look for wildcard match -showcopy option
      if {[regexp {^\-+sh?o?w?c} $x]} {
         if {$::opt_copy != ""} {
            log_warning "setup ignoring previous option $::opt_copy, using $x"
         } 
         set ::opt_copy "-showcopy"
         continue
      }

      # NB: The remaining options are independant of each other.

      # Look for wildcard match -keepempty option
      if {[regexp {^\-+k} $x]} {
         if {$::opt_keep != ""} {
            log_warning "setup ignoring previous option $::opt_keep, using $x"
         } 
         set ::opt_keep "-keepempty"
         continue
      }

      # Look for wildcard match -trace option
      if {[regexp {^\-+t} $x]} {
         if {$::opt_trace != ""} {
            log_warning "setup ignoring previous option $::opt_trace, using $x"
         } 
         set ::opt_trace "-trace"
         continue
      }

      # Unknown option
      log_error "setup invalid option: $x"
      log_info "\nFor more info, type: tclsh $::self -h"
      exit 1
   }
   # puts "setup opt_cleanup=$::opt_cleanup opt_copy=$::opt_copy opt_keep=$::opt_keep opt_trace=$::opt_trace"

   # Choose log file name based on known options of different OS.
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
      log_error "setup could not open $::out_file catch_msg=$catch_msg"
      exit 1
   }
   # puts "out_file=$::out_file out=$::out"

   # Log start date/time, calling parms.
   log_info "\n[timestamp] $::self setup starting src_dir=$::src_dir dest_dir=$::dest_dir options=$opt_string TCL=$::tcl_patchLevel"

   # Check src directory exists.
   # NB: Do NOT put braces around $::src_dir!
   if {[file isdirectory "$::src_dir"]} {
      # log_info "setup found src_dir=$::src_dir OK"
   } else {
      log_error "setup src_dir=$::src_dir not found!"
      exit 1
   }

   # Check src_dir is different from dest_dir
   if {[string tolower $::src_dir] == [string tolower $::dest_dir]} {
      log_error "setup dest_dir=$::dest_dir must be DIFFERENT from src_dir=$::src_dir!"
      exit 1
   }

   # Create destination directory if required. If high level destination
   # directory cant be created, we stop the script here.
   # NB: If dest_dir is something like "2", TCL makes the new directory in pwd!
   # NB: Do NOT put braces around $::dest_dir here!
   if {[file isdirectory "$::dest_dir"]} {
      # log_info "setup found dest_dir=$::dest_dir OK"
   } else {
      if {$::opt_copy == "-showcopy"} {
         log_info "setup would have created dest_dir=$::dest_dir, did NOT due to $::opt_copy"
      } else {
         # NB: We DO need braces around $::dest_dir for mkdir!
         set catch_resp [catch "file mkdir {$::dest_dir}" catch_msg]
         if {$catch_resp == 0} {
            log_info "setup created dest_dir=$::dest_dir OK"
         } else {
            log_error "setup could not create dest_dir=$::dest_dir $catch_msg"
            exit 1
         }
      }
   }
}

#==================== timestamp ========================================
# Returns current date & time formatted as: YYYY/MM/DD HH:MM
#=======================================================================
proc timestamp { } {

   return [clock format [clock seconds] -format "%Y/%m/%d %H:%M"]
}

#==================== Main program =====================================
# Main program
#=======================================================================

# Run setup routine
setup

# Test code
# log_info "aaaa bbbb"
# log_error "cccc dddd"
# log_warning "eeee ffff"
# exit

# Recursively get all file names in the source directory, along with
# the modified date/time info. Data is stored in file_array.
rec_find "$src_dir"
log_info "[timestamp] $self main starting differential copy $src_dir, $total_files files, $subdir_cnt subdir,\
   $errors errors, $warnings warnings"
log_info "misc: $hidden_files_cnt hidden files, $hidden_subdir_cnt hidden dir, $empty_dir_found empty dir found,\
   $empty_dir_deleted empty dir deleted, $empty_dir_kept empty dir kept, $curly_cnt curly err,\
   $fulldisk_cnt fulldisk err, $noacc_cnt noacc err, $unexp_cnt unexp err"

# Save current rec_find stats for final exit message stats.
set total_src_files $total_files
set total_src_subdir $subdir_cnt
set total_src_hidden_files $hidden_files_cnt
set total_src_hidden_subdir $hidden_subdir_cnt

# Check if each source file exists in the destination_directory and is up to date.
set cur_dest_dir "" ;# keep track of current dest_dir
for {set i 1} {$i <= $total_files} {incr i} {

   # Get source file info
   set src_path $file_array($i,name)
   set src_subdir [file dirname "$src_path"]
   if {![regexp {/$} $src_subdir]} {
      set src_subdir "${src_subdir}/" ;# add trailing / if missing
   }
   set src_file [file tail $src_path]
   set src_sec $file_array($i,modified_sec)
   set src_date_time $file_array($i,modified_date_time)
   set src_byte_size $file_array($i,byte_size)
   # log_info "main i=$i src_path=$src_path  src_subdir=$src_subdir src_file=$src_file src_sec=$src_sec src_date_time=$src_date_time src_byte_size=$src_byte_size"

   # Use string range to correctly get dest_subdir.
   set dest_subdir [string range $src_subdir $src_dir_len end]
   set dest_subdir "${dest_dir}${dest_subdir}" ;# dont need to insert /
   
   # Set the destination file full path name.
   set dest_path "${dest_subdir}${src_file}" ;# dont need to insert /
   # log_info "main i=$i dest_path=$dest_path dest_subdir=$dest_subdir"

   # Check for path conversion errors.
   if {[string tolower $src_path] == [string tolower $dest_path]} {
      log_error "main i=$i src_path=$src_path EQ dest_path, something went seriously wrong!"
      incr unexp_cnt
      continue
   }

   # If necessary, try just once to create the required destination directory.
   if {$cur_dest_dir != $dest_subdir} {
      # log_info "main checking dest_subdir=$dest_subdir"
      # NB: Do NOT put braces around $dest_subdir here!
      if {[file isdirectory "$dest_subdir"]} {
         # log_info "dest_subdir=$dest_subdir already exists, OK"
      } else {
         if {$opt_copy == "-showcopy"} {
            log_info "main would have created dest_subdir=$dest_subdir, did NOT due to $opt_copy"
         } else {
            # NB: We DO need braces around $dest_subdir for mkdir!
            set catch_resp [catch "file mkdir {$dest_subdir}" catch_msg]
            if {$catch_resp == 0} {
               log_info "main created dest_subdir=$dest_subdir OK"
            } else {
               log_error "main could not create dest_subdir=$dest_subdir, $catch_msg"
            }
         }
      }

      # Remember the most recent dest_dir we tried to create. This helps us
      # avoid hammering the destination volume with multiple duplicate requests.
      set cur_dest_dir $dest_subdir
   }

   # Does dest_path exist? If yes, get modified date/time/size info. Decide if
   # the file needs to be copied or not.
   set copy_file "no"
   set reason ""
   if {[file exists "$dest_path"]} {
      # Get dest_path mtime.
      set catch_resp [catch "set dest_sec \[file mtime {$dest_path}\]" catch_msg]
      if {$catch_resp != 0} {
         set dest_sec 0
         set status [get_status $catch_msg]
         log_error "main i=$i mtime $dest_path $catch_msg ($status)"
      }

      # Create human readable date/time.
      # set dest_sec "abc" ;# test code
      set catch_resp [catch "set dest_date_time \[clock format $dest_sec -format \"%Y/%m/%d %H:%M:%S\"\]" catch_msg]
      if {$catch_resp != 0} {
         set dest_date_time "-/-/- -:-:-"
         set status [get_status $catch_msg]
         log_error "main i=$i date/time $dest_path $catch_msg ($status)"
      }

      # Now get dest_path size, in bytes.
      set catch_resp [catch "set dest_byte_size \[file size {$dest_path}\]" catch_msg]
      if {$catch_resp != 0} {
         set dest_byte_size -1
         set status [get_status $catch_msg]
         log_error "main i=$i size $dest_path $catch_msg ($status)"
      }
      # log_info "main i=$i dest_sec=$dest_sec dest_date_time=$dest_date_time dest_byte_size=$dest_byte_size"

      # NB: For flash drives, the copied file often has a file modify time of 1
      # or 2 seconds after the source file. I suspect that this occurs because
      # the write process on flash drives is slower than a hard drive. Anyway, I 
      # allow for 3 seconds tolerance in the modify times to accomodate flash
      # drives.

      # We also want to take daylight saving time into account, allowing 1 hour 
      # either way in the computations. My USB flash drives dont seem to auto
      # adjust at the spring & fall daylight time change overs, and end up recopying
      # all files twice a year when nothing has really changed. Very annoying!

      # We need both absolute value differences in file date/times and positive/negative
      # values for making the decisions to copy or not and why. In case of errors, we log
      # the errors and set values to 0 which will result in NO action. When the user 
      # investigates or reruns, the correct action will be taken.
      # set src_sec "xyz" ;# test code
      # set dest_sec "def" ;# test code
      # delta_sec1 needs to be positive value only
      set catch_resp [catch "set delta_sec1 \[expr abs($src_sec - $dest_sec)\]" catch_msg] 
      if {$catch_resp != 0} {
         set delta_sec1 0
         set status [get_status $catch_msg]
         log_error "main i=$i delta_sec1 src_sec=$src_sec dest_sec=$dest_sec $catch_msg ($status)"
      }
      # set delta_sec1 "hij" ;# test code
      # Allow for 1 hour difference due to daylight savings.
      # delta_sec2 needs to be positive value only
      set catch_resp [catch "set delta_sec2 \[expr abs($delta_sec1 - 3600)\]" catch_msg] 
      if {$catch_resp != 0} {
         set delta_sec2 0
         set status [get_status $catch_msg]
         log_error "main i=$i delta_sec2 src_sec=$src_sec dest_sec=$dest_sec delta_sec1=$delta_sec1 $catch_msg ($status)"
      }
      # delta_sec3 can be positive or negative value, used to determine if file is older vs newer.
      set catch_resp [catch "set delta_sec3 \[expr $src_sec - $dest_sec\]" catch_msg] 
      if {$catch_resp != 0} {
         set delta_sec3 0
         set status [get_status $catch_msg]
         log_error "main i=$i delta_sec3 src_sec=$src_sec dest_sec=$dest_sec $catch_msg ($status)"
      }

      # If files have approximately the same date/time info, then check file sizes.
      set slop_sec 3 ;# mtime tolerance in seconds
      if {$delta_sec1 <= $slop_sec || $delta_sec2 <= $slop_sec} {
         # Date/time look OK, now check file sizes.
         if {$src_byte_size != $dest_byte_size} {
            set copy_file "yes"
            set reason "size src: $src_byte_size dest: $src_byte_size"
         }

      # If src_file is newer, set the copy flag.
      } elseif {$delta_sec3 > $slop_sec} {
         set copy_file "yes"
         set reason "updated src: $src_date_time dest: $dest_date_time delta: $delta_sec3 sec"

      # If dest_file is newer, look for -force option to decide the appropriate action.
      } elseif {$delta_sec3 < -$slop_sec} {
         if {$opt_copy == "-force"} {
            # Force the copy of older source file to the destination.
            set copy_file "yes"
            set reason "force src: $src_date_time dest: $dest_date_time delta: $delta_sec3 sec"
         } else {
            # Warn the user, dont copy the file.
            log_warning "main i=$i dest: $dest_path $dest_date_time NEWER THAN src: $src_path $src_date_time, delta $delta_sec3 sec, NOT copied!"
            set reason "warning NEWER dest" ;# for -trace info
         }

      # Fatal error case. If ever go here, script stops, game over!
      } else {
         log_error "main i=$i Should NEVER go here, src_sec=$src_sec dest_sec=$dest_sec delta_sec=$delta_sec1,$delta_sec2,$delta_sec3, src_byte_size=$src_byte_size dest_byte_size=$dest_byte_size copy_file=$copy_file reason=$reason src_date_time=$src_date_time dest_date_time=$dest_date_time src_path=$src_path dest_path=$dest_path"
         cleanup
      }

      # Add optional trace info.
      if {$opt_trace != ""} {
         log_info "main i=$i src_sec=$src_sec dest_sec=$dest_sec delta_sec=$delta_sec1,$delta_sec2,$delta_sec3, src_byte_size=$src_byte_size dest_byte_size=$dest_byte_size copy_file=$copy_file reason=$reason src_date_time=$src_date_time dest_date_time=$dest_date_time src_path=$src_path dest_path=$dest_path"
      }

   } else {
      # dest_path is NOT there, set copy flag.
      set copy_file "yes"
      set reason "new"

      # Add optional trace info.
      if {$opt_trace != ""} {
         log_info "main i=$i src_sec=$src_sec src_byte_size=$src_byte_size copy_file=$copy_file reason=$reason src_date_time=$src_date_time src_path=$src_path dest_path=$dest_path"
      }
   }
   
   # Copy the file if necessary.
   if {$copy_file == "yes"} {
      if {$opt_copy == "-showcopy"} {
         # Log what we would have copied, but didnt!
         log_info "main i=$i Would have copied $src_path ($reason), did NOT due to $opt_copy"
         # Counters will be shown as "NOT copied"
         if {$reason == "new"} {
            incr new_files
         } else {
            incr updated_files
            if {[regexp {^force} $reason]} {
               incr force_files
            }
         }

      } else {
         log_info "main i=$i copying $src_path ($reason)"
         # NB: filenames are allowed to have embedded dollar signs, so put curly
         # braces around filenames in copy command to avoid evaluation errors.
         # NB: filenames can also have [text] which looks like TCL command
         set catch_resp [catch "file copy -force {$src_path} {$dest_path}" catch_msg]
         # set catch_resp 1 ;# test code
         # set catch_msg abcd ;# test code
         if {$catch_resp == 0} {
            # Increment counters on copy success only!
            if {$reason == "new"} {
               incr new_files
            } else {
               incr updated_files
               if {[regexp {^force} $reason]} {
                  incr force_files
               }
            }
         } else {
            set status [get_status $catch_msg]
            log_error "main i=$i Could not copy to $dest_path ($reason), $catch_msg ($status)"
         }
      }
   } 
}

# Optional show or delete old files in the destination directory.
# puts "opt_cleanup=$opt_cleanup"
if {$opt_cleanup != ""} {
   if {$opt_cleanup == "-delete"} {
      log_info "Deleting old files..."
   } else {
      log_info "Showing old files..."
   }

   # Unset existing file_array entries
   set temp [array names file_array]
   # puts "temp=$temp"
   foreach item $temp {
      # puts "unset file_array: $item"
      unset file_array($item)
   }

   # Recursively get files from destination directory
   set total_files 0
   set subdir_cnt 0
   set hidden_files_cnt 0
   set hidden_subdir_cnt 0
   rec_find "$dest_dir"

   # Show or remove files in destination directory that are not in the source directory.
   for {set i 1} {$i <= $total_files} {incr i} {

      # Get dest file info
      set dest_path $file_array($i,name)
      set dest_subdir [file dirname "$dest_path"]
      if {![regexp {/$} $dest_subdir]} {
         set dest_subdir "${dest_subdir}/" ;# add trailing / if missing
      }
      set dest_file [file tail $dest_path]
      # log_info "main i=$i dest_path=$dest_path dest_subdir=$dest_subdir dest_file=$dest_file"

      # Use string range to correctly get src_subdir.
      set src_subdir [string range $dest_subdir $dest_dir_len end]
      set src_subdir "${src_dir}${src_subdir}" ;# dont need to insert /
   
      # Set the source file full path name.
      set src_path "${src_subdir}${dest_file}" ;# dont need to insert /
      # log_info "main i=$i  src_path=$src_path  src_subdir=$src_subdir"

      # Check for path conversion errors.
      if {[string tolower $src_path] == [string tolower $dest_path]} {
         log_error "main i=$i dest_path=$dest_path EQ src_path, something went seriously wrong!"
         incr unexp_cnt
         continue
      }

      # If file is in the src_dir, leave it alone!
      # NB: Do NOT put braces around $src_path here!
      if {[file exists $src_path]} {
         # puts "main i=$i FOUND src_path=$src_path"
         continue

      } elseif {$opt_cleanup == "-delete"} {
         log_info "main i=$i DELETING: dest_path=$dest_path"
         set catch_resp [catch "file delete {$dest_path}" catch_msg]
         if {$catch_resp == 0} {
            incr ::deleted
         } else {
            set status [get_status $catch_msg]
            log_error "main i=$i Could not delete dest_path=$dest_path, $catch_msg ($status)"
         }

      } else {
         log_info "main i=$i SHOWOLD: dest_path=$dest_path"
         incr ::showold
      }
   }
}

# Cleanup routine.
cleanup
