# Proc - check if file exists. Set return code.
###############################################
proc checkFile {fileName} {
    
    if {[file exists $fileName] == 1} {
       puts "\nfile exists: $fileName\n"	
       return 0
       } else {
               puts "\nfile does not exist: $fileName\n"	
	       return -code error 1
    }
}
