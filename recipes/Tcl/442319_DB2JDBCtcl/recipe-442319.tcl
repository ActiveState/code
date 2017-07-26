###########################################################
# Connect to DB2 using Type 4 Java driver.
###########################################################

puts "\nexecuting [info script]\n"

# make script drive independent.

set drive [lindex [file split [info nameofexecutable]] 0 ] 

puts "\nproclib = $drive/scripts/TCL/proclib"

########################################################  
# Source packages. 
########################################################  

package require java

######################################
# Proc - check mq listener. 
######################################
proc db2Connect { serverName databaseName portNumber driverType username password sqlQuery } {

   puts "\ndb2Connect \n"

   # import required classes 
   java::import java.sql.Connection
   java::import java.sql.DriverManager
   java::import java.sql.ResultSet
   java::import java.sql.SQLWarning
   java::import java.sql.Statement
   java::import java.sql.ResultSetMetaData 
   java::import com.ibm.db2.jcc.DB2Driver
   java::import com.ibm.db2.jcc.DB2Driver

   # load db2 driver .
   java::call Class forName com.ibm.db2.jcc.DB2Driver

   # set the connection url.

   append url jdbc:db2://
   append url $serverName
   append url :
   append url $portNumber
   append url /
   append url $databaseName
   append url :
   append url user\=$username
   append url \;
   append url password\=$password
   append url \;

   puts "connection URL is:  $url\n"   
   
   set ConnectionI [ java::call DriverManager getConnection $url ] 

   puts "transaction isolation level is [ $ConnectionI getTransactionIsolation ] \n"

   puts "Create query\n" 

   set opt1 [java::field ResultSet TYPE_SCROLL_INSENSITIVE]
   set opt2 [java::field ResultSet CONCUR_READ_ONLY ]

   set StatementI [ $ConnectionI createStatement $opt1 $opt2 ]
   
   $StatementI execute $sqlQuery   

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

   puts "Close Connections\n" 

   $ResultSetI   close
   $ConnectionI  close

}
######################################
# Main Control.
######################################

# build tcl classpath

append x $drive/IBM/SQLLIB/java/db2jcc.jar;
append x $drive/IBM/SQLLIB/java/db2jcc_license_cu.jar;
append x $drive/IBM/SQLLIB/java/db2jcc_license_cisuz.jar;

set env(TCL_CLASSPATH) $x

puts "\nTCL_CLASSPATH = [ array get env TCL_CLASSPATH ]\n"

set reportFile   $drive/reports/notify/mqConnect.txt
set reportFileId [ open $reportFile w ] 

set serverName   yourserver
set databaseName yourDatabase
set portNumber   50000
set driverType   4
set username     yourUserid
set password     yourPassword

set sqlQuery "select * from abcd.customer_table where char(customer) like '12345%'"  

db2Connect $serverName $databaseName $portNumber $driverType $username $password $sqlQuery 
