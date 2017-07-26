# 
# Install Virtual Hosts.
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
	lappend returnList                 $2
    }

    puts \n

    return $returnList   
}
####################################################################
# Create Virtual Host.
####################################################################
proc installVHost { virtualhostName hostAliases cellId } {

   global AdminConfig 

   foreach i $hostAliases {

       set hostname  [ list hostname [ lindex  [split $i : ] 0 ] ]
       set port      [ list port     [ lindex  [split $i : ] 1 ] ]

       set hostAlias [ list $hostname $port ]

       lappend hostAliasList $hostAlias  

   }
 
   set aliases  [ list aliases $hostAliasList ]
   set name     [ list name $virtualhostName ]

   set attrList [ list $name $aliases ] 

   if { [ catch {$AdminConfig create VirtualHost $cellId $attrList} r ] == 0 } {
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

# the first argument is the logical name
# the remaining arguments are the host aliases.

set virtualhostName [ lindex $argv 0 ]
set hostAliases     [ lrange $argv 1 end ] 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodeId [ lindex [ $AdminConfig list Node ] 0 ]

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

if { [ catch { installVHost $virtualhostName $hostAliases $cellId } r ] == 0 } {
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
