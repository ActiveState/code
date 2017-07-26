#!/bin/sh
#\
    exec tclsh "$0" "$@"


#changes filenames in caps to lowercase

#show usage info if no option is given
if {[llength $argv] == 0} {
    puts "Usage: hi2lo file1 file2..."
}

foreach file $argv {  
    #check if the string contains any UPPERCASE letter
    if {[string is lower $file]} {
	puts "File '$file' is already in lowercase."
    } else {
		set filelow [string tolower $file]   	
		#check if the file is present on the disk
		if {[file exists $file]} { 
		    #check if the two names are different
	    	if {[string compare $file $filelow]} {		
				puts "From: $file To: $filelow"
				exec cp $file $filelow
		    }
		}
    }
}
