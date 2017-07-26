@echo off

echo ***************************************************
echo * Export WebSphere configuration on %COMPUTERNAME%
echo ***************************************************

setlocal

set OUTPUTFILE=c:\scripts\websphere\exported_xml\%computername%.xml 

call wscp -p c:\scripts\websphere\wscp_properties.txt ^
          -f c:\scripts\tcl\exportnode.tcl ^
          -- %OUTPUTFILE% ^
	     %COMPUTERNAME%

endlocal

----------------------------------------------------------------

exportnode.tcl

# 
# Export WebSphere configuration
#

######################################
# Set Variables
######################################

set outputfile 		[lindex $argv 0]
set computername	[lindex $argv 1]

puts "\n outputfile    = $outputfile \n"
puts "\n computername  = $computername \n"

######################################
# Procedures
######################################

######################################
# Proc - check if dir path exists. 
######################################
proc check_file {file_name} {
    
    set dirname  [file dirname $file_name] 
    
    if {[file exists $dirname] == 1} {
       puts "\n directory $dirname exists \n"
       } else {
	       error "\n directory $dirname does not exist.  Create $dirname before running this script \n"
    }
}
######################################################
# Proc - export node
######################################################
proc exportnode {outputfile computername} {

    set und _
    set filename [file rootname   $outputfile]
    set ext      [file extension  $outputfile]
    set outputfile_name [file join $filename$und[clock seconds]$ext]

    puts "\n exporting WebSphere Configuration on $computername to $outputfile_name \n"
    
    if {[catch [XMLConfig export $outputfile_name] result_var] == 0} {
       puts "$result_var"
       } else {
       error $result_var
    }
}
######################################
# Control block"
######################################

#########################################
# Check if output file directories exist.
#########################################

check_file $outputfile

######################################
# Export WebSphere Configuration
######################################

exportnode $outputfile $computername

puts "######################################"
puts "# END."
puts "######################################"
