@echo off

setlocal

set dbDir=D:\CloudScapeDatabases\yourdb
set backupDir=D:\CloudScapeDatabasesBackups

echo ###################################################
echo # Create db on %computername%
echo ###################################################

set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derby.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbyclient.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbynet.jar
set CLASSPATH=%CLASSPATH%;d:\IBM\Cloudscape_10.1\lib\derbytools.jar

d:\tclBlendSun\bin\jtclsh.bat d:\SCRIPTS\TCL\JACL\cloudscape\backupDb.tcl %dbDir% %backupDir%

endlocal

===========================================================================

# 
# Backup DB. 
#
####################################################################
# Patrick Finnegan 23/11/2005.  V1. 
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
# Lock database - read only. 
####################################################################
proc lockDb { dbDir ConnectionI } {

   puts "\n**********"
   puts "Lock DB $dbDir"
   puts "**********\n"

   global env 
   global null

   # create statement object

   java::try {
       
       set StatementI [ $ConnectionI createStatement ]

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Database: $url"
       return -code error $e
   } 

   set sql "CALL SYSCS_UTIL.SYSCS_FREEZE_DATABASE()"

   java::try {
       
       $StatementI executeUpdate $sql

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Database: $url"
       return -code error $e
   } 
   

}

####################################################################
# UnLock database. 
####################################################################
proc unlockDb { dbDir ConnectionI } {

   puts "\n**********"
   puts "Unlock DB $dbDir"
   puts "**********\n"

   global env 
   global null

   # create statement object

   java::try {
       
       set StatementI [ $ConnectionI createStatement ]

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Database: $url"
       return -code error $e
   } 

   set sql "CALL SYSCS_UTIL.SYSCS_UNFREEZE_DATABASE()"

   java::try {
       
       $StatementI executeUpdate $sql

   } catch {SQLException SQLExceptionI } {

     catchSqlException $SQLExceptionI 
         
   } catch {TclException e } {
       puts "TCl Exception during Create Database: $url"
       return -code error $e
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

if {$argc < 2} {
        return -code error "\nerror - not enough arguments supplied.\nSupply database directory and backup directory."
}

set dbDir       [ lindex $argv 0 ]
set backupDir   [ lindex $argv 1 ] 
set backupDBDir [ file join $backupDir [ file tail $dbDir ] ] 

# If the backup directory does not exist create it.

if { [ file exists backupDBDir ] } {

    set ok true

} else {

     file mkdir $backupDBDir

}

puts "\ndbdir     = $dbDir"
puts "backupDir = $backupDBDir\n"

set computerName  $::env(COMPUTERNAME)
set traceFile     [ file join $dbDir backupDb\.log ]
set traceFileId   [ open $traceFile a ]

checkFile $dbDir 
checkFile $backupDir

set header   "$computerName: Backup Cloudscape Db: $dbDir"
reportHeader $traceFileId $header $traceFile

set computerTime [clock format [clock seconds] -format "%d-%m-%Y_%H.%M.%S"]

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

    lappend msg " ***** Connected to $dbDir successfully *****. " 

    set ConnectionI $r

    if { [ catch { lockDb $dbDir $ConnectionI } r ] == 0 } {

       lappend msg " ***** Database $dbDir locked successfully *****." 
       
       puts "\n**********"
       puts "File Copy"
       puts "**********\n"

       append backupDBDir _ $computerTime 

       file mkdir $backupDBDir 

       if { [ catch { file copy $dbDir $backupDBDir } r ] == 0 } {

	   lappend msg " ***** Copied $dbDir \n        to $backupDBDir successfully." 

       } else {

          puts $r
          lappend msg $r

       }

       if { [ catch { unlockDb $dbDir $ConnectionI } r ] == 0 } {
    
	   lappend msg " ***** Database $dbDir unlocked successfully *****." 
    
       } else {

          puts $r
          lappend msg $r

       } 

    } else {    

       puts $r
       lappend msg $r

    }

} else {

    puts $r
    lappend msg $r

}

foreach i $msg  {

   puts "\n$i\n"
   puts $traceFileId $i

}

close $traceFileId	

set subject       "$computerName: Backup Db: $dbDir"
set emailAddress  you@youremail.com
sendSimpleMessage $emailAddress $subject $traceFile
