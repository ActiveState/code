# 
# Install Virtual Host.
#
####################################################################
# Patrick Finnegan 01/09/2004.  V1. 
####################################################################

####################################################################
# List installed virtual hosts.
####################################################################
proc showList { a } {

    puts "\nList installed virtual hosts"
    puts "\**********************\n"

    foreach e $a {
	regexp {(.*)(\(cells.*)} $e 1 2 3
	puts [ format "%-5s %-50s"  " "  $2 ]
#	puts [ format "%-10s %-50s\n" " "  $3 ]
	lappend returnList                 $2
    }

    puts \n

    return $returnList   
}
####################################################################
# Create Virtual Host.
####################################################################
proc installVHost { virtualhostName virtualHost nodeId } {

   global AdminConfig 

   set port     [ list port     9081 ] 
   set host     [ list hostname $virtualHost ]

   set aliases  [ list aliases [ list [list $port $host ]]]

   set name     [ list name     $virtualhostName ]
  
   set attrList [ list          $name $aliases ]

   if { [ catch {$AdminConfig create VirtualHost $nodeId $attrList} r ] == 0 } {
        puts "************************************"
        puts "$virtualhostName virtual host created successfully."
        puts "************************************\n"
   } else {
           puts "\nfailed to create $virtualhostName virtual host\n"
           puts "************************************\n"
	   return -code error $r
   }

}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 2} {
        return -code error "error - no arguments supplied.  Supply virtual host name"
        puts "no arguments"
}

set virtualhostName [lindex $argv 0]
set virtualHost     [lindex $argv 1]
set nodeName        [ exec hostname ] 
set nodeId          [ $AdminConfig getid /Node:$nodeName/ ]

#######################################################################
# List virtual hosts check if target virtual host already exists.
# If so delete it and recreate.
#######################################################################
set vHosts [ $AdminConfig list VirtualHost ]

catch { showList $vHosts } r

catch {lsearch $r $virtualhostName } r 

if { $r == -1 } {
    set continue true 
} else { 
        set vHostId [ $AdminConfig getid /VirtualHost:$virtualhostName/ ]
        catch { $AdminConfig remove $vHostId } r
	puts $r
}
####################################################################
# Install virtual host  
####################################################################
if { [ catch { installVHost $virtualhostName $virtualHost $nodeId } r ] == 0 } {
    puts "************************************"
    puts "$virtualhostName installed successfully"
    puts "************************************\n"
    puts "\n###### Admin Config Save ######\n"
    $AdminConfig save
} else {
        puts "\n$virtualhostName failed to install\n"
        puts $r 
        puts "************************************\n"
}
####################################################################
# List virtual hosts to verify install 
####################################################################

set vHosts [ $AdminConfig list VirtualHost ]

catch { showList $vHosts } r
