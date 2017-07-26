@echo off

setlocal

echo ###################################################
echo # Create db on %computername%
echo ###################################################

set dbDir=D:\CloudScapeDatabases\yourDB

set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derby.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbyclient.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbynet.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbytools.jar

d:\tclblendSun\bin\jtclsh.bat D:\scripts\TCL\JACL\cloudscape\createCloudScapeDB.tcl %dbDir%

endlocal

==============================================================

# 
# create cloudscape db 
####################################################################
# Patrick Finnegan 15/11/2005.  V1. 
####################################################################

####################################################################
# Get Cloudscape connection.
####################################################################
proc createDB { dbName traceFile } {

   puts "\n**********"
   puts "createDB"
   puts "**********\n"

   global env 
   global null

   # load client driver

   java::call Class forName org.apache.derby.jdbc.ClientDriver

   append url jdbc:derby
   append url ":" 
   append url $dbName
   append url ";" 
   append url create\=true
   append url ";" 
   append url traceFile=$traceFile

   puts "\n connection URL is:  $url\n"   

   java::try {
       
       set ConnectionI [ java::call DriverManager getConnection $url ] 

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Database: $url"
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

     if { $sqlCode       != $null } { lappend msgList "sql code is:       \t$sqlCode"       }
     if { $sqlMessage    != $null } { lappend msgList "sql message is:    \t$sqlMessage "   }
     if { $errorCode     != $null } { lappend msgList "error code is:     \t$errorCode"     }
     if { $sqlState      != $null } { lappend msgList "sql state is:      \t$sqlState"      }

     set SQLExceptionI [ $SQLExceptionI getNextException ]

   }


   return -code error $msgList

}
####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 1} {
        return -code error "\nerror - not enough arguments supplied.\nSupply db directory."
}

set dbName    [ lindex $argv 0 ] 
append traceFile [ file tail $dbName ] _log\.txt  
set traceFile [ file join $dbName $traceFile ]

puts "\n Database Name:\t $dbName"  
puts " Log File:\t $traceFile\n"  

#call java package 

package require java

# import required classes 
java::import java.sql.Connection
java::import java.sql.DriverManager
java::import java.sql.ResultSet
java::import java.sql.SQLWarning
java::import java.sql.Statement
java::import java.sql.ResultSetMetaData 
java::import org.apache.derby.drda.NetworkServerControl
java::import org.apache.derby.jdbc.ClientDriver

puts "\nimported classes are:\n"

foreach i [java::import] {
   
  puts [ format "%-5s %-50s" " " $i ] 

}

# build tcl classpath

set null [ java::null ]

if { [ catch { createDB $dbName $traceFile } r ] == 0 } {

    set doNothing true 

} else {

    puts $r 
    exit 1   

}
