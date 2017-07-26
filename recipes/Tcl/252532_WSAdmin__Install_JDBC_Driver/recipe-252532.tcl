####################################################################
# List available JDBC templates.
####################################################################
proc listTemplates {args} {

    puts "\nList JDBC templates\n"

    global AdminConfig 

    foreach e [ $AdminConfig listTemplates JDBCProvider [ lindex $args 0 ] ] {
	regexp {(.*)(\(templates)} $e 1 2 3
	puts [ format "%-5s %-50s\n" " " $2 ]
	lappend returnList               $2
    }

    return $returnList   

}
####################################################################
# List installed JDBC providers.
####################################################################
proc showList { a } {

    puts "\nList installed JDBC drivers\n"

    foreach e $a {
	regexp {(.*)(\(cells.*)} $e 1 2 3
	puts [ format "%-5s %-50s\n"  " "  $2 ]
	puts [ format "%-10s %-50s\n" " "  $3 ]
	lappend returnList                 $2
    }

    return $returnList   
}
####################################################################
# StartServer.
####################################################################
proc startServer { serverName } {

    if {[catch {exec net start "IBM WebSphere Application Server V5 - $serverName"} result_var] == 0}  {
	   return [list 0 $result_var]
       } else {
	   set msg "CHECK C:\\IBM\\WebSphere\\AppServer\\logs\\$serverName for errors"
	   return [list 1 $result_var msg] 
    }
}
####################################################################
# Install JDBC provider.
####################################################################
proc installJDBCDriver {serverNameId classpath implementationClassName dbDriver} {

   puts "\nInstall $dbDriver JDBC driver\n"

   global AdminConfig 

   set classpath               [list classpath $classpath]
   set implementationClassName [list implementationClassName $implementationClassName]
   set name                    [list name $dbDriver]

   set attrList                [list $classpath $implementationClassName $name]

   catch {$AdminConfig create JDBCProvider $serverNameId $attrList} r

}
####################################################################
# Show properties of Installed JDBC provider.
####################################################################
proc showProperties {dbDriver} {

   puts "\nShow properties for $dbDriver JDBC driver\n"

   global AdminConfig 

   set dbDriverId [ $AdminConfig getid /JDBCProvider:$dbDriver/ ]
   set propList   [ $AdminConfig showall $dbDriverId ]

   puts "\n$dbDriver Properties\n" 

   foreach e $propList {
	puts [ format "%-5s %-30s %-20s" " " [lindex $e 0] [lindex $e 1] ]
   }
}
####################################################################
# Main Control.
####################################################################

set nodeName   "yournode"
set serverName "server1"
set dbDriver   "DB2ConnectionPoolDataSource"

set nodeId       [$AdminConfig getid /Node:$nodeName/]
puts "\nnodeid = $nodeId\n"

set serverNameId [$AdminConfig getid /Node:$nodeName/Server:$serverName/]
puts "\nserverNameId = $serverNameId\n"

####################################################################
# List available JDBC templates.  Optional. 
####################################################################

listTemplates 

#######################################################################
# List jdbc providers and check if target jdbc provider already exists.
# If so delete it and recreate
#######################################################################

set jdbcproviders [ $AdminConfig list JDBCProvider ]

catch { showList $jdbcproviders } r

catch {lsearch $r $dbDriver} r 

if { $r == -1 } {
    set continue true 
} else { 
        puts "\nDelete $dbDriver JDBC driver\n"
        set dbDriverId [$AdminConfig getid /JDBCProvider:$dbDriver/]
        catch {$AdminConfig remove $dbDriverId} r
	puts $r
}
####################################################################
# Install JDBC Driver.
####################################################################

set classpath               c:/IBM/SQLLIB/java/db2java.zip 
set implementationClassName COM.ibm.db2.jdbc.DB2ConnectionPoolDataSource 

installJDBCDriver $serverNameId $classpath $implementationClassName $dbDriver
####################################################################
# List jdbc providers to verify install 
####################################################################

set jdbcproviders [ $AdminConfig list JDBCProvider ]

catch { showList $jdbcproviders } r

####################################################################
# Save Admin config. 
####################################################################

$AdminConfig save

####################################################################
# Restart Server. 
####################################################################

puts "\nStop $serverName"
catch [$AdminControl stopServer $serverName] r

puts "\nStart $serverName"

catch [startServer $serverName] r 

####################################################################
# Show properties of installed driver.
####################################################################

showProperties $dbDriver

####################################################################
# The end.
####################################################################

puts [ format "\n %-30s %-30s" " " "*** THE END ***\n" ]
