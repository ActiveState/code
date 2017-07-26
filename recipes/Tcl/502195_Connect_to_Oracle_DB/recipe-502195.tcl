###########################################################
# Connect to Oracle using Type 4 Java driver.
###########################################################

#########################################################  
## Source packages. 
#########################################################  
#
package require java

#################################################################
# putsLog with timestamp.
####################################################################
proc putsLog { a } {

    set host [ info host ]

    set compTime [clock format [clock seconds] -format "%Y-%m-%d-%H.%M.%S"]

    puts "\[$host:$compTime\] $a"

}
#######################################
## Proc - oracleConnect. 
#######################################
proc oracleConnect { serverName databaseName portNumber driverType username password sqlQuery } {

   putsLog "proc - [info level 0 ]"

   # import required classes 
   java::import java.sql.Connection
   java::import java.sql.DriverManager
   java::import java.sql.ResultSet
   java::import java.sql.SQLWarning
   java::import java.sql.Statement
   java::import java.sql.ResultSetMetaData 
   java::import java.sql.DatabaseMetaData 
   java::import oracle.jdbc.OracleDatabaseMetaData

   # load database driver .
   java::call Class forName oracle.jdbc.OracleDriver 

   # set the connection url.


   append url jdbc:oracle:thin
   append url :
   append url $username
   append url /
   append url $password
   append url "@"
   append url $serverName
   append url :
   append url $portNumber
   append url :
   append url $databaseName

   putsLog "connection URL is:  $url\n"   
   
   set ConnectionI [ java::call DriverManager getConnection $url ] 

   putsLog "transaction isolation level is [ $ConnectionI getTransactionIsolation ]"

   putsLog "#########################################"
   putsLog "### Database connection details"
   putsLog "#########################################"

   # get the database metadata information.
   #Retrieves a DatabaseMetaData object that contains metadata about the database
   #to which this Connection object represents a connection.

   set DatabaseMetaDataI [ $ConnectionI getMetaData ]

   putsLog [ $DatabaseMetaDataI getDatabaseProductName ]
   putsLog [ $DatabaseMetaDataI getDatabaseProductVersion ]
   putsLog "database version [ $DatabaseMetaDataI getDatabaseMajorVersion ]\.[ $DatabaseMetaDataI getDatabaseMinorVersion ]"
   putsLog "driver version   [ $DatabaseMetaDataI getDriverName ] [ $DatabaseMetaDataI getDriverMajorVersion ]\.[ $DatabaseMetaDataI getDriverMinorVersion ]"
   putsLog "jdbc version     [ $DatabaseMetaDataI getJDBCMajorVersion  ]\.[ $DatabaseMetaDataI getJDBCMinorVersion  ]"
   putsLog "connect username [ $DatabaseMetaDataI getUserName ]"
   putsLog "transaction isolation level is [ $ConnectionI getTransactionIsolation ] \n"

   # get a list of table names in database.
   # if there are no tables the results set is empty.  

   set opt1 [java::field ResultSet TYPE_SCROLL_INSENSITIVE]

   set ResultSetI [ $DatabaseMetaDataI getCatalogs ]

   set ResultSetMetaDataI [ $ResultSetI getMetaData ] 
  
   set columnCount        [ $ResultSetMetaDataI getColumnCount ]

   putsLog "Column Count is $columnCount"

   set i 1

   while { $i <= $columnCount } {

       set columnName [ $ResultSetMetaDataI getColumnName $i ]
      
       lappend columnList $columnName

       incr i 
   }    

   unset i

   putsLog $columnList 

   $ResultSetI  close 
   $ConnectionI close

}
######################################
# Main Control.
######################################

putsLog "executing [info script]"

# make script drive independent.

set drive [lindex [file split [info nameofexecutable]] 0 ] 

set reportFile   C:\\reports\\oracleConnect.txt

set reportFileId [ open $reportFile w ] 

set serverName   xxxx
set databaseName xxxx
set portNumber   1234
set driverType   4
set username     xxxx
set password     xxxx

set sqlQuery "select * from aaaa.bbbb where char(customer) like '287554%'"  

oracleConnect $serverName $databaseName $portNumber $driverType $username $password $sqlQuery 
