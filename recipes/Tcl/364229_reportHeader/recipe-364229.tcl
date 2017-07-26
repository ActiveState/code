######################################################
# Proc - write report file header
######################################################
proc reportHeader {reportfile header outputFile} {
   
    set computer_name $::env(COMPUTERNAME)
    set computer_time [clock format [clock seconds] -format "%d-%m-%Y %H.%M.%S"]
    
    puts $reportfile "###################################################################################"
    puts $reportfile "# $header on $computer_name at = $computer_time."   
    puts $reportfile "#                      *****  "
    puts $reportfile [format "%-20s %s" {# Author:} {Patrick Finnegan}]
    puts $reportfile [format "%-20s %s" {# Report File:} $outputFile]
    puts $reportfile "###################################################################################\n"
}
