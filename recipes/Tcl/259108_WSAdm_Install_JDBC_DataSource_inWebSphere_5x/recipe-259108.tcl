# 
# Install DataSource connection userid.
# Install DataSource.
# Save Config
# Restart Server
# Test connection
#
####################################################################
# Patrick Finnegan 22/12/2003.  V1. 
####################################################################

####################################################################
# List installed DataSources. 
####################################################################
proc showList { a } {

    puts "\nList installed DataSources\n"

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
# Install DataSource.
####################################################################
proc installDataSource {dbDriverId dataSource} {

   puts "\nInstall $dataSource\n"

   global AdminConfig 

#  set general properties. 
   catch {setProperties $dataSource} r 

   set attrList $r 

#  install datasource with general properties. 
   catch {$AdminConfig create DataSource $dbDriverId $attrList} r
   puts "\n$r\n" 

#  set custom properties for new datasource.
   set dataSourceId [ $AdminConfig getid /DataSource:$dataSource/ ]

   catch {setCustomProps $dataSource} r 

   set attrList $r 

#  create propertySetId then assign custom attributes. 
   set propertySetId [ $AdminConfig create J2EEResourcePropertySet $dataSourceId {} ]

   foreach e $attrList {
       $AdminConfig create J2EEResourceProperty $propertySetId $e
   }

}
####################################################################
# Set general properties for DataSource.
####################################################################
proc setProperties {dataSource} {

   global alias 

   puts "\n setProperties - DataSource is $dataSource\n" 

# set up general properties

   set authDataAliasList             [list authDataAlias              $alias]
   set authMechanismPreferenceList   [list authMechanismPreference    BASIC_PASSWORD]
   set descriptionList               [list description                "Developer Database"]
   set nameList                      [list name                       DB1]
   set jndiNameList                  [list jndiName                   db_db1]
   set providerList                  [list provider                   DB2ConnectionPoolDataSource]
   set relationalResourceAdapterList [list relationalResourceAdapter  "WebSphere Relational Resource Adapter"]
   set statementCacheSizeList        [list statementCacheSize         10]
   set datasourceHelperClassnameList [list datasourceHelperClassname  com.ibm.websphere.rsadapter.DB2DataStoreHelper]

# set up mapping properties 

   set authDataAliasList             [ list authDataAlias      $alias ]
   set mappingConfigAliasList        [ list mappingConfigAlias DefaultPrincipalMapping ]

   set mappingList                   [ list $authDataAliasList $mappingConfigAliasList]
   
# set up connection pool 

    set agedTimeout        [list agedTimeout                    0          ]
    set connectionTimeout  [list connectionTimeout              1800       ]
    set maxConnections     [list maxConnections                 10         ]
    set minConnections     [list minConnections                 1          ]
    set purgePolicy        [list purgePolicy                    EntirePool ]
    set reapTime           [list reapTime                       180        ]
    set unusedTimeout      [list unusedTimeout                  1800       ]
    
    set connectionPoolList [list  $agedTimeout       \
                                  $connectionTimeout \
                                  $maxConnections    \
                                  $minConnections    \
                                  $purgePolicy       \
                                  $reapTime          \
                                  $unusedTimeout     \

                           ] 

   set attrs [list $nameList                      \
                   $jndiNameList                  \
                   $descriptionList               \
                   $authDataAliasList             \
                   $authMechanismPreferenceList   \
                   $statementCacheSizeList        \
                   $datasourceHelperClassnameList \
                   $authDataAliasList             \
                   [ list mapping $mappingList ]  \
                   [ list connectionPool $connectionPoolList ] ]

   return $attrs
}
####################################################################
# Set custom properties. 
####################################################################
proc setCustomProps {dataSource} {

   puts "setCustomProps - DataSource is $dataSource" 

    set name                     [ list name       databaseName        ]
    set required                 [ list required   true                ]
    set type                     [ list type       "java.lang.String"  ]
    set value                    [ list value      DB1                 ]

    set custom1                  [ list $name $required $type $value   ]
    
    set name                     [ list name       enableSQLJ          ]
    set required                 [ list required   false               ]
    set type                     [ list type       java.lang.Boolean   ]
    set value                    [ list value      false               ]

    set custom2                  [ list $name $required $type $value   ]

    set name                     [ list name           description      ]
    set required                 [ list required       false            ]
    set type                     [ list type           java.lang.String ]
    set value                    [ list value          "Developer DataBase"] 

    set custom3                  [ list $name $required $type $value   ]

    set name                     [ list name          portNumber         ] 
    set required                 [ list required      false              ] 
    set type                     [ list type          java.lang.Integer  ] 
    set value                    [ list value         " "                ] 

    set custom4                  [ list $name $required $type $value   ]

    set name                     [ list name          connectionAttribute ]
    set required                 [ list required      false               ]
    set type                     [ list type          java.lang.String    ]
    set value                    [ list value         cursorhold=0        ]

    set custom5                  [ list $name $required $type $value   ]

    set name                     [ list name          loginTimeout        ]
    set required                 [ list required      false               ]
    set type                     [ list type          java.lang.Integer   ]
    set value                    [ list value         0                   ]

    set custom6                  [ list $name $required $type $value   ]

    set name                     [ list name          enableMultithreadedAccessDetection]
    set required                 [ list required      false                             ]
    set type                     [ list type          java.lang.Boolean                 ]
    set value                    [ list value         false                             ]

    set custom7                  [ list $name $required $type $value   ]

    set name                     [ list name          preTestSQLString    ]
    set required                 [ list required      false               ]
    set type                     [ list type          java.lang.String    ]
    set value                    [ list value         " "                   ]

    set custom8                  [ list $name $required $type $value ]
 
    set customPropsList [ list $custom1 $custom2 $custom3 $custom4 $custom5 $custom6 $custom7 $custom8 ]
 
    return $customPropsList
}
####################################################################
# Create Security Object for database connection.
####################################################################
proc createSecurityObj {alias userid password description} {

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

   puts "\nremove duplicate entries if any\n"

   set i 0

   while { $i < [llength $JAASentries] } {

      puts " index is [ lindex [ $AdminConfig show [lindex $JAASentries $i ] ] 0 ]"
      catch { lsearch [ lindex [ $AdminConfig show [lindex $JAASentries $i ] ] 0 ] $alias } r

      if { $r == -1 } {
	  puts "\n no match for $alias\n"
      } else { 
	    puts "\n **** Delete $alias **** \n"
            
	    catch { $AdminConfig remove [ lindex $JAASentries $i ] } r
	    puts $r
      }
      incr i
   }

# set attributes for userid

   set alias       [list alias       $alias ]
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
# Test Connection.
# Note: Test Connection method assumes that userid and password have already been set in repository.
####################################################################
proc testConnection {dataSource dbDriver} {

   puts "\ntestConnection - dataSource is $dataSource\n" 

   global AdminConfig 
   global AdminControl 

   set dataSourceId [$AdminConfig getid /JDBCProvider:$dbDriver/DataSource:$dataSource/]

   catch {$AdminControl testConnection $dataSourceId} r
   puts "\ntest connection result is $r\n"
}
####################################################################
# Main Control.
####################################################################

set nodeName   "yournode"
set serverName "server1"
set dbDriver   "DB2ConnectionPoolDataSource"
set dataSource "DB1"

set nodeId       [$AdminConfig getid /Node:$nodeName/]

set serverNameId [$AdminConfig getid /Node:$nodeName/Server:$serverName/]

set dbDriverId   [ $AdminConfig getid /JDBCProvider:$dbDriver/ ]

####################################################################
# Create DB connection Id.
# Must exist before assignment to datasource. 
####################################################################

set alias       $nodeName/userAlias
set userid      userid
set password    yourPassword
set description "DB2 Connection ID for DB1" 

createSecurityObj $alias $userid $password $description

####################################################################
# List DataSources and check if target datasource already exists.
# If so delete it and recreate
####################################################################

set datasources [ $AdminConfig list DataSource ]

catch { showList $datasources } r

catch { lsearch $r $dataSource } r 

if { $r == -1 } {
    set continue true 
    puts "\n no match for $dataSource\n"
} else { 
        puts "\nDelete $dataSource \n"
        set dataSourceId [$AdminConfig getid /DataSource:$dataSource/]
        catch {$AdminConfig remove $dataSourceId} r
	puts $r
}
####################################################################
# Install target DataSource under target DB driver.
####################################################################

installDataSource $dbDriverId $dataSource 

####################################################################
# List datasources to verify install 
####################################################################

set datasources [ $AdminConfig list DataSource ]

catch { showList $datasources } r

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
# Test Connection to DataSource 
####################################################################
#
testConnection $dataSource $dbDriver 

####################################################################
# The end.
####################################################################

puts [ format "\n %-30s %-30s" " " "*** THE END ***\n" ]
