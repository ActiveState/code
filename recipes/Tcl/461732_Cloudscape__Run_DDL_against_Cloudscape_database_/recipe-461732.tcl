@echo off

setlocal

set dbDir=D:\CloudscapeDatabases\yourdb
set schema=yourschema
set sqlFile=D:\scripts\cloudscape\SQL\createWASPerformanceTable.sql

echo ###################################################
echo # Run SQL on %computername%
echo ###################################################

set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derby.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbyclient.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbynet.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbytools.jar

d:\tclBlendSun\bin\jtclsh.bat D:\scripts\TCL\JACL\cloudscape\runBatchSQL.tcl %dbDir% %schema% %sqlFile% 

endlocal

====================================================================

# 
# Run SQl. 
#
####################################################################
# Patrick Finnegan 28/11/2005.  V1. 
# This script runs multiple sql statements delimited by ";" specified in the input file.
# Comments lines "--" are excluded. 
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

   # load client driver

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
# parse the sql file. 
####################################################################
proc parseSql { sql } {

   puts "\n**********"
   puts "Parse SQL"
   puts "**********\n"

   global env 
   global null

   # split sql statements on newline eliminating blank lines.
   set sqlList  [ lsearch -all -inline -exact -not [ split $sql "\n" ] "" ]

   # eliminate comment lines.
   set statements [ lsearch -all -inline -not -regexp $sqlList "(?ni)^--" ] 

   # concat the statement list, delimit by ";", eliminate spaces.
   set sqlParsed [ split [ eval concat $statements ] ";" ]
   set sqlParsed [ lsearch -all -inline -exact -not $sqlParsed "" ]

   puts "sqlParsed = $sqlParsed"

   return $sqlParsed
   
}

####################################################################
# Run the sql statements. 
####################################################################
proc runSQL { sql ConnectionI schema } {

   puts "\n**********"
   puts "Run SQL"
   puts "**********\n"

   global env 
   global null

   # Get Metadata.

   set  DatabaseMetaDataI [ $ConnectionI getMetaData ]  

   if { [ $DatabaseMetaDataI supportsBatchUpdates ] } { 
       
       puts "SQL Batching is supported"

   } else {  

       puts "SQL Batching is NOT supported"
       return -code error

   }

   # Disable Auto Commit.

   $ConnectionI setAutoCommit false  

   # create statement object

   java::try {
       
       set StatementI [ $ConnectionI createStatement ]

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Statement"
       return -code error $e
   } 

   # Set Schema.

   java::try {
       
       $StatementI executeUpdate "set schema $schema"

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Execute Statement"
       return -code error $e
   } 
   
   # Clear the statement object.

   java::try {
       
       $StatementI clearBatch

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Execute Statement"
       return -code error $e
   } 

   set x 1 

   foreach i $sql {

      puts "\nStatement $x :\n\n$i\n" 
      $StatementI addBatch $i 

      incr x
   }

   java::try {
       
       $StatementI executeBatch 

   } catch {BatchUpdateException BatchUpdateExceptionI } {

     catchBatchUpdateException $BatchUpdateExceptionI 
         
   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Execute Statement"
       return -code error $e
   } 

   java::try {
       
       set WarningsI [ $StatementI getWarnings ]

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Execute Statement"
       return -code error $e
   } 

   if { $WarningsI == $null } { 
       
       puts "no SQL warnings " 
       
   } else {
       
       puts " SQL warnings: [ $Warnings toString ] "

   }
   
   # Commit changes.

   $ConnectionI commit 

}
####################################################################
# proc - batchUpdateException. 
####################################################################
proc catchBatchUpdateException { batchUpdateExceptionI } {

   global AdminConfig 
   global AdminControl
   global Help
   global null

   puts "\n**********"
   puts "catchBatchUpdateException"
   puts "**********\n"

   set sqlCode       [ $batchUpdateExceptionI toString         ]
   set sqlMessage    [ $batchUpdateExceptionI getMessage       ]
   set errorCode     [ $batchUpdateExceptionI getErrorCode     ] 
   set sqlState      [ $batchUpdateExceptionI getSQLState      ] 

   if { $sqlCode    != $null } { lappend msgList "sql code is:       \t$sqlCode" }
   if { $sqlMessage != $null } { lappend msgList "sql message is:    \t$sqlMessage" }
   if { $errorCode  != $null } { lappend msgList "error code is:     \t$errorCode" }
   if { $sqlState   != $null } { lappend msgList "sql state is:      \t$sqlState\n" }

   set SQLExceptionI [ $batchUpdateExceptionI getNextException ]  

   while { $SQLExceptionI != $null } {

     set sqlCode       [ $SQLExceptionI toString         ]
     set sqlMessage    [ $SQLExceptionI getMessage       ]
     set errorCode     [ $SQLExceptionI getErrorCode     ] 
     set sqlState      [ $SQLExceptionI getSQLState      ] 
     set nextException [ $SQLExceptionI getNextException ]

     if { $sqlCode       != $null } { lappend msgList "sql code is:       \t$sqlCode"       }
     if { $sqlMessage    != $null } { lappend msgList "sql message is:    \t$sqlMessage "   }
     if { $errorCode     != $null } { lappend msgList "error code is:     \t$errorCode"     }
     if { $nextException != $null } { lappend msgList "next exception is: \t$nextException" }
     if { $sqlState      != $null } { lappend msgList "sql state is:      \t$sqlState"      }

   set SQLExceptionI [ $SQLExceptionI getNextException ]  

   }

   return -code error $msgList

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

if {$argc < 3 } {
        return -code error "\nerror - not enough arguments supplied.\nSupply db directory, schema and sql file."
}

set dbDir   [ lindex $argv 0 ]
set schema  [ lindex $argv 1 ]
set sqlFile [ lindex $argv 2 ]

set computerName  $::env(COMPUTERNAME)

checkFile $dbDir 
checkFile $sqlFile 

set sql [ read [ open $sqlFile r ] ]

puts "\nSQL:\n$sql\n"

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

    if { [ catch { runSQL [ parseSql $sql ] $ConnectionI $schema } r ] == 0 } {

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
