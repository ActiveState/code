# 
# Install J2C Auth ID.
#
####################################################################
# Patrick Finnegan 23/05/2005.  V1. 
####################################################################

####################################################################
# Create Security Object for database connection.
####################################################################
proc createSecurityObj {j2cAlias userid password description} {

   puts "\nCreate Security Object\n" 

   global AdminConfig 
  
   puts "\nList installed JAASAuthData authentication entries\n"

   set JAASentries [ $AdminConfig list JAASAuthData ] 

   foreach e $JAASentries {

      set subList [ $AdminConfig show $e ]

      foreach e $subList {
         puts [ format "%-5s %-30s %-20s" " " [ lindex $e 0 ] [ lindex $e 1 ] ]
      }

      puts "\n" 
   }

   puts "\nRemove Possible Duplicate Entries\n"

   set i 0

   while { $i < [llength $JAASentries] } {

      puts " index is [ lindex [ $AdminConfig show [lindex $JAASentries $i ] ] 0 ]"
      catch { lsearch [ lindex [ $AdminConfig show [lindex $JAASentries $i ] ] 0 ] $j2cAlias } r

      if { $r == -1 } {
	  puts "\n no match for $j2cAlias\n"
      } else { 
	    puts "\n **** Delete $j2cAlias **** \n"
            
	    catch { $AdminConfig remove [ lindex $JAASentries $i ] } r
	    puts $r
      }
      incr i
   }

# set attributes for userid

   set alias       [list alias       $j2cAlias ]
   set description [list description $description ]
   set userid      [list userId      $userid ]
   set password    [list password    $password ]

   set jaasAttrs   [list $alias $description $userid $password]

#  create JAASAuthData object under security parent

   $AdminConfig create JAASAuthData [$AdminConfig list Security] $jaasAttrs

   puts "\nList installed JAASAuthData authentication entries - confirm change \n"

   foreach e [ $AdminConfig list JAASAuthData ] {

      set subList [ $AdminConfig show $e ]

      foreach e $subList {
         puts [ format "%-5s %-30s %-20s" " " [ lindex $e 0 ] [ lindex $e 1 ] ]
      }

      puts "\n" 
   }
}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 4 } {
        return -code error "error - not enough arguments supplied.  Supply j2cAlias description userid password"
}

puts "\n Check"

set j2cAlias       [lindex $argv 0 ]
set j2cDesc        [lindex $argv 1 ]
set userid         [lindex $argv 2 ]
set password       [lindex $argv 3 ] 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodes  [ $AdminConfig list Node ]

# delete the manager node from the list.

set manIndex   [ lsearch -glob $nodes *Manager* ]
set nodeId     [ lindex [ lreplace $nodes $manIndex $manIndex ] 0 ]

# delete the manager node from the list.

set cellName [ $AdminConfig showAttribute $cellId name ]
set nodeName [ $AdminConfig showAttribute $nodeId name ]

puts "\n Cell Name:	$cellName"
puts "\n Node Name:	$nodeName \n"

puts "  j2cAlias       = $j2cAlias     "
puts "  j2cDesc        = $j2cDesc      "
puts "  userid         = $userid       "
puts "  password       = $password     "

####################################################################
# Create DB connection Id.
# Must exist before assignment to datasource. 
####################################################################

createSecurityObj $j2cAlias $userid $password $j2cDesc

####################################################################
# Save Admin config. 
####################################################################

$AdminConfig save

puts [ format "\n %-30s %-30s" " " "*** THE END ***\n" ]
