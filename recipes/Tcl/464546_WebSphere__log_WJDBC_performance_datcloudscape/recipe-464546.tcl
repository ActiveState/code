@echo off

setlocal

TITLE "GETJDBCINFO"

set host=yourserver
set dataBase="D:/DERBYDatabases/yourdatabase"
set schema="yourschema"
set driver="DB2XADataSource"

set server=yourserver

call :GETPMIINFO

goto :EOF

:GETPMIINFO
echo ###################################################
echo # Get PMI info for %server%
echo ###################################################

command.com /c

pushd d:\IBM\WebSphere\AppServer\bin

call d:\IBM\WebSphere\AppServer\bin\wsadmin -conntype SOAP^
                                            -port 8879^
					    -host %host%^
					    -user user^
					    -password password^
                       -f d:\scripts\websphere\jacl\getJDBCINFO.tcl %server% %database% %schema% %driver%


endlocal 

===========================================================================

# 
# Get JDBC PMI info for server. 
# NB: server must be running and PMI must be switched on.
#
####################################################################
# Patrick Finnegan 11/11/2005.  V1. 
####################################################################

####################################################################
# Get Cloudscape connection.
####################################################################
proc dbconnect { databaseName } {

   puts "\n**********"
   puts "dbconnect"
   puts "**********\n"

   global env 
   global null

   # load client driver.
   java::call Class forName org.apache.derby.jdbc.ClientDriver

   append url jdbc:derby
   append url ":" 
   append url "//" 
   append url $::env(com.ibm.ws.scripting.host)
   append url ":" 
   append url "1527" 
   append url "/" 
   append url $databaseName 

   puts "\n connection URL is:  $url\n"   

   java::try {
       
       set ConnectionI [ java::call DriverManager getConnection $url ] 

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
	 
   } catch {TclException e } {
       puts "TCl Exception to prepare statement $e"
       return -code error
   }

   puts "transaction isolation level is [ $ConnectionI getTransactionIsolation ] \n"

   java::lock $ConnectionI 

   return $ConnectionI 

}
####################################################################
# proc - get JDBC details 
####################################################################
proc getJDBCInfo { nodeName serverName ConnectionI schema driver } {

   global AdminConfig 
   global AdminControl
   global null
   global Help

   puts "\n**********"
   puts "getJDBCInfo"
   puts "**********\n"

   puts "\nget the performance mbean for the server - should be just one.\n"

   append queryString "WebSphere:*,node="
   append queryString $nodeName
   append queryString ",process="
   append queryString $serverName
   append queryString ",type=Perf"

   puts "\n query string is: $queryString \n"

   set perfMbean [ $AdminControl queryNames $queryString ]

   if { $perfMbean == $null || [ string length $perfMbean] == 0 } {
       
       puts "\n $serverName is not running or PMI is not enabled for $serverName. \n"

       return 

   } else {

       set donothing true 

   }

   puts "\nget the JDBC Bean.\n"

   unset queryString 

   append queryString "WebSphere:*,node="
   append queryString $nodeName
   append queryString ",name="
   append queryString $driver
   append queryString ",process="
   append queryString $serverName
   append queryString ",type=JDBCProvider"

   puts "\n query string is: $queryString \n"

   set JDBCMbean [ $AdminControl queryNames $queryString ]

   #puts "\n JDBCMbean: $JDBCMbean \n"
   puts "\n length JDBCMbean: [ llength $JDBCMbean ] \n"
   
   if { $JDBCMbean == $null || [ string length $JDBCMbean] == 0 } {
       
       puts "\n $serverName JDBC is not running \n"

       return 

   } else {

       set donothing true 

   }

   set JDBCMbeanO [ $AdminControl makeObjectName $JDBCMbean ]

   set boolean [ java::new Boolean recursive ]
   # NB: brackets around array object. 
   set parramsArray    [ java::new {Object[]} {2} [ list $JDBCMbeanO $boolean ] ]
   set signaturesArray [ java::new {String[]} {2} [ list javax.management.ObjectName java.lang.Boolean ] ]

   set perfMbeanO [ $AdminControl makeObjectName $perfMbean ]

   #get the stats list from the performance bean
   puts "get the stats list from the performance bean"

   set JDBCInfo [ $AdminControl invoke_jmx $perfMbeanO "getStatsString" $parramsArray $signaturesArray   ] 

   if { $JDBCInfo == $null || [ string length $JDBCInfo ] == 0 } {
       
       puts "\n $serverName: No JDBC stats available \n"

       return 

   } else {

       set donothing true 

   }

   set JDBCInfoString [ $JDBCInfo toString ] 

   #get PMI data sub list.
   set e4        [ lindex $JDBCInfoString 3 ]  
   set dataList  [ lindex $e4 1 ]  
   set dataListL [ llength $dataList ]  

   # sort in id order
   set dataList [ lsort -dictionary -index 0 $dataList ] 

   #set topParms [ lindex $dataList 0 ]  
   set topParms [ lindex $JDBCInfoString 1 ]

   set width 60

   set x1  [ lindex [ lindex [ lindex $topParms 1 ] 0 ] 0 ]
   set x2  [ lindex [ lindex [ lindex $topParms 1 ] 0 ] 1 ]
   puts    [ format "%-${width}s %s"  $x1 $x2 ]

   lappend valuesList $x2
      
   set x1  [ lindex [ lindex [ lindex $topParms 1 ] 1 ] 0 ]
   set x2  [ lindex [ lindex [ lindex $topParms 1 ] 1 ] 1 ]
   puts    [ format "%-${width}s %s"  $x1 $x2 ]

   lappend valuesList $x2

   set x1        "Time"
   set x2        [ clock format [ clock seconds ] -format "%Y-%m-%d %H:%M:%S" ]
   puts          [ format "%-${width}s %s"  $x1 $x2 ]

   lappend valuesList $x2

   set x 0 
   set y [ llength $dataList ]

   while { $x < $y } {

      set e                [ lindex $dataList $x ]

      set idIndex          [ lsearch -glob $e {*Id*} ]
      set id               [ lindex $e $idIndex ]

      set pmiDataInfoIndex [ lsearch -glob $e {*PmiDataInfo*} ]
      set pmiDataInfo      [ lindex $e $pmiDataInfoIndex ]

      set nl               [ eval concat [ join $e ] ]
      set commentIndex     [ lsearch -glob $nl {*Comment*} ]
      set comment          [ lindex [ lindex $nl $commentIndex ] 1 ]
      
      set valueIndex       [ lsearch -glob $e {*Value*} ]
      set value            [ lindex $e $valueIndex ] 

      set value [ lrange $value 1 end ]

      set lengthValue [ llength $value ]

      if { $lengthValue == "1" || $lengthValue == "4" } {

         set p [ lindex [ lindex $value 0 ] 1 ]

      } else {

         set p [ lindex [ lindex $value 2 ] 1 ]

      }

      puts [ format "%-${width}s %s"  $comment $p ]

      lappend valuesList $p

      unset p
      incr x 

   }

   #write data to DB2. 
   
   writeData $ConnectionI $valuesList $schema  

   unset valuesList 
}
####################################################################
# proc - write data to database. 
####################################################################
proc writeData { ConnectionI valuesList schema } {

   global AdminConfig 
   global AdminControl
   global null

   puts "\n**********"
   puts "writeData"
   puts "**********\n"

   set opt1 [java::field ResultSet TYPE_SCROLL_INSENSITIVE]
   set opt2 [java::field ResultSet CONCUR_READ_ONLY ]

   #puts "\n values list is $valuesList\n"

   set statement "insert into $schema.wasperformJDBC values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

   java::try {
       
       set StatementI [ $ConnectionI prepareStatement $statement ]

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
	 
   } catch {TclException e } {
       puts "TCl Exception to prepare statement $e"
       return -code error
   }

   set x 1

   foreach i $valuesList {

         $StatementI setString $x $i  

	 #puts $i  

         incr x

   }

   #puts "execute sqlQuery"

   java::try {
       
       $StatementI executeUpdate   

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception to prepare statement $e"
       return -code error
   }

}
####################################################################
# proc - sqlException. 
####################################################################
proc catchSqlException { SQLExceptionI } {

   global AdminConfig 
   global AdminControl
   global Help
   global null

   puts "\n**********"
   puts "catchSqlException"
   puts "**********\n"

   set sqlCode       [ $SQLExceptionI toString         ]
   set sqlMessage    [ $SQLExceptionI getMessage       ]
   set errorCode     [ $SQLExceptionI getErrorCode     ] 
   set sqlState      [ $SQLExceptionI getSQLState      ] 

   if { $sqlCode    != $null } { lappend msgList "sql code is:       \t$sqlCode" }
   if { $sqlMessage != $null } { lappend msgList "sql message is:    \t$sqlMessage" }
   if { $errorCode  != $null } { lappend msgList "error code is:     \t$errorCode" }
   if { $sqlState   != $null } { lappend msgList "sql state is:      \t$sqlState\n" }

   while { $SQLExceptionI != $null } {

       
     puts "\nget SQL Exception\n" 

     set sqlCode       [ $SQLExceptionI toString         ]
     set sqlMessage    [ $SQLExceptionI getMessage       ]
     set errorCode     [ $SQLExceptionI getErrorCode     ] 
     set sqlState      [ $SQLExceptionI getSQLState      ] 

     set SQLExceptionI [ $SQLExceptionI getNextException ]

     if { $sqlCode       != $null } { lappend msgList "sql code is:       \t$sqlCode"       }
     if { $sqlMessage    != $null } { lappend msgList "sql message is:    \t$sqlMessage "   }
     if { $errorCode     != $null } { lappend msgList "error code is:     \t$errorCode"     }
     if { $sqlState      != $null } { lappend msgList "sql state is:      \t$sqlState"      }

   }

   return -code error $msgList

}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 4 } {
        return -code error "error - not enough arguments supplied.  Supply server name, database, schema, driver."
}

# import required classes 
java::import java.sql.Connection
java::import java.sql.DriverManager
java::import java.sql.ResultSet
java::import java.sql.SQLWarning
java::import java.sql.Statement
java::import java.sql.ResultSetMetaData 
java::import org.apache.derby.jdbc.ClientDriver

puts "imported classes are:\n"

foreach i [java::import] {
   
  puts [ format "%-5s %-50s" " " $i ] 

}
       
# Assume one cell, one deployment manager node and one application node. 

set cellId [ lindex [ $AdminConfig list Cell ] 0 ]
set nodes  [ $AdminConfig list Node ]

# delete the manager node from the list.

set manIndex   [ lsearch -glob $nodes *Manager* ]
set nodeId     [ lindex [ lreplace $nodes $manIndex $manIndex ] 0 ]

# get name attribute for cell and application node

set cellName [ $AdminConfig showAttribute $cellId name ]
set nodeName [ $AdminConfig showAttribute $nodeId name ]

set serverName   [ lindex $argv 0 ]
set databaseName [ lindex $argv 1 ]
set schema       [ lindex $argv 2 ]
set driver       [ lindex $argv 3 ]

set null [ java::null ]
global null

if { [ catch { dbconnect $databaseName } r ] == 0 } {

   while {1} { 

     after 30000
     getJDBCInfo $nodeName $serverName $r $schema $driver

   }

   $r close

} else {

    puts $r 
    exit 1   

}
