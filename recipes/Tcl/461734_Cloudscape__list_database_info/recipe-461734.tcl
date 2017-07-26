@echo off

setlocal

set dbDir=D:\DERBYDatabases\yourDB

echo ###################################################
echo # Run SQL on %computername%
echo ###################################################

set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derby.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbyclient.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbynet.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbytools.jar

d:\tclBlendSun\bin\jtclsh.bat D:\scripts\TCL\JACL\cloudscape\listDBinfo.tcl %dbDir%  
endlocal

=====================================================================

# 
# List DB Info. 
#
####################################################################
# Patrick Finnegan 28/11/2005.  V1. 
####################################################################

puts "\n **** executing [info script] **** \n"

# make script drive independent.

set drive [lindex [file split [info script]] 0 ] 

puts "\n proclib = $drive/scripts/TCL/proclib"

source $drive/scripts/TCL/proclib/checkFile_proc.tcl
source $drive/scripts/TCL/proclib/smtp_proc.tcl
source $drive/scripts/TCL/proclib/reportHeader_proc.tcl

####################################################################
# Connect to database. 
####################################################################
proc connectDB { dbDir } {

   puts "\n**********"
   puts "connectDB"
   puts "**********\n"

   global env 
   global null

   # load db2 driver

   java::call Class forName org.apache.derby.jdbc.ClientDriver

   append url jdbc:derby
   append url ":" 
   append url "//" 
   append url $::env(COMPUTERNAME)
   append url ":" 
   append url "1527" 
   append url "/" 
   append url $dbDir

   puts "\n connection URL is:  $url\n"   

   java::try {
       
       set ConnectionI [ java::call DriverManager getConnection $url ] 

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Database: $url"
       return -code error
   } 

   java::lock $ConnectionI

   return $ConnectionI

}
####################################################################
# Get DB Info. 
####################################################################
proc getDBInfo { ConnectionI } {

   puts "\n**********"
   puts "Get DB Info"
   puts "**********\n"

   global env 
   global null

   # create statement object

   java::try {
       
       set StatementI [ $ConnectionI createStatement ]

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Statement"
       puts $e
       return -code error $e
   } 

   set sql "select * from sys.sysschemas"

   java::try {
       
       $StatementI executeQuery $sql 

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Execute Statement"
       puts $e
       return -code error $e
   } 

   java::lock $StatementI

   displayResults $StatementI

   set sql "select * from sys.systables"

   java::try {
       
        $StatementI executeQuery $sql 

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Execute Statement"
       return -code error $e
   } 

   java::lock $StatementI

   displayResults $StatementI
}
####################################################################
# displayResults 
####################################################################
proc displayResults { StatementI } {

   puts "\n**********"
   puts "displayResults"
   puts "**********\n"

   global env 
   global null

   set ResultSetI         [ $StatementI getResultSet ]  

   puts "get a list of return columns\n" 

   set ResultSetMetaDataI [ $ResultSetI getMetaData ] 
  
   set columnCount        [ $ResultSetMetaDataI getColumnCount ]

   set i 1

   while { $i <= $columnCount } {

       set columnName [ $ResultSetMetaDataI getColumnName $i ]
      
       lappend columnList $columnName

       incr i 
   }    

   unset i

   puts "loop over the results set and print column name, column value.\n" 

   while { [ $ResultSetI next ] == 1 } {

       foreach i $columnList {

	  puts [ format "%-5s %-30s %-s" " " "$i" "[ $ResultSetI getString $i ]" ]

       } 

       puts [ format "\n%-5s \n" [ string repeat "#" 50] ]

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

set dbDir   [ lindex $argv 0 ]

set computerName  $::env(COMPUTERNAME)

checkFile $dbDir 

#call java package 

package require java

set null [ java::null ]

# import required classes 
java::import java.sql.Connection
java::import java.sql.DriverManager
java::import java.sql.SQLWarning
java::import java.sql.Statement
java::import org.apache.derby.jdbc.ClientDriver

puts "\nimported classes are:\n"

foreach i [java::import] {
   
  puts [ format "%-5s %-50s" " " $i ] 

}

if { [ catch { connectDB $dbDir } r ] == 0 } {

    set ConnectionI $r

    lappend msgList "***** Connected to $dbDir *****"

    if { [ catch { getDBInfo $ConnectionI } r ] == 0 } {

       lappend msgList "***** SQL run successfully *****."

    } else {

       lappend msgList "***** SQL ERROR *****."
       lappend msgList $r

    }

} else {

    lappend msgList "\n***** Failed to connect to $dbDir *****.\n"
    lappend msgList $r

}

foreach i $msgList {

   puts $i 

}
