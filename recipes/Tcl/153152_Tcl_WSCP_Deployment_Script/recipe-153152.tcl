@echo off 
echo ################################################
echo # Create Enterprise App on %computername%
echo ################################################

::################################################
::# This is a windows shell script which calls the WSCP shell to execute the Tcl script. 
::# The Tcl script is designed to be portable across environments hence the parameters are set here and then fed to the script.
:: EARFILE		- location of deployable ear file
:: APPNAME  		- application name
:: DEFAPPSERVER		- default app server.  Note: if this is used within the Tcl script it overides specific app server mappings.   	 
:: GROUPROLESFILE	- roles to user groups mapping file.	
:: NETSENDMSG		- displayable error message.	
:: NETSENDFILE          - specifies users who receive net send error message. 
:: HOSTFILE		- maps web modules to virtual hosts
:: SERVERFILE		- maps web/ejb modules to application servers.	
::################################################

set EARFILE=c:\Enterprise_Apps\h2.ear 
set APPNAME=H2 
set DEFAPPSERVER="/Node:%computername%/ApplicationServer:Default Server/" set USERROLESFILE=c:\userrole_mapping.txt
set GROUPROLESFILE=c:\grouprole_mapping.txt
set NETSENDMSG="Create H2 app failed on %computername% at %date% %time%"
set NETSENDFILE=C:\SCRIPTS\DB2\emailfiles\netsend.txt
set HOSTFILE=c:\vhost_mapping.txt
set SERVERFILE=c:\server_mappings.txt

:: "^" is a dos shell continuation character" 

call wscp -p c:\scripts\websphere\wscp_properties.txt^
          -f c:\SCRIPTS\tcl\create_enterprise_app.tcl^
          -- %EARFILE%^
             %APPNAME%^
             %DEFAPPSERVER%^
             %USERROLESFILE%^
             %NETSENDMSG%^
             %NETSENDFILE%^
             %HOSTFILE%^
             %SERVERFILE%^
             %GROUPROLESFILE%



-----------------------------------------------------------------

create_enterprise_app.tcl script.


############################################### 
# Create Websphere Enterprise App. 
############################################### 

######################################################
# Proc - assign parameters.
######################################################
proc assign_param {argv} {

    
    global  earFile
    global  nodeId
    global  appName
    global  defAppServer
    global  userrolesFile
    global  grouprolesFile
    global  netSendMsg
    global  netSendFile
    global  vhostsfile
    global  serverfile

    set earFile        [lindex $argv 0]
    set appName        [lindex $argv 1]
    set defAppServer   [lindex $argv 2]
    set userrolesFile  [lindex $argv 3]
    set netSendMsg     [lindex $argv 4]
    set netSendFile    [lindex $argv 5]
    set vhostsfile     [lindex $argv 6]
    set serverfile     [lindex $argv 7]
    set grouprolesFile [lindex $argv 8]

    set nodeId [Node list]

    puts "NodeID                 = $nodeId"
    puts "App Name               = $appName"
    puts "Default App Server     = $defAppServer"
    puts "User Roles File        = $userrolesFile"
    puts "netSendMsg             = $netSendMsg"
    puts "netSendFile            = $netSendFile"
    puts "earFile                = $earFile"
    puts "vhostsfile             = $vhostsfile"
    puts "serverfile             = $serverfile"
    puts "Group Roles File       = $grouprolesFile"
}
######################################
# Proc - check number of arguments
######################################
proc check_args {argc} {
    
    if {$argc < 0} {
	    error "Argument Count is Zero.  No arguments supplied."
	   } else {
		puts ""
		puts "argument count = $argc"
		puts ""
    }

}
######################################
# Proc - check if dir path exists.  If not create the directory.
######################################
proc check_file {file_name netSendMsg} {
    
    if {[file exists $file_name] == 1} {
       puts "File location confirmed for:  $file_name"
       } else {
	       error "$file_name does not exist.  Create $file_name before running this scipt"
	       netsend $netSendMsg
    }
}
######################################################
# Proc - get net send list
######################################################
proc get_netsend {netsendfile_id} {

    global netsend_list

    while {[gets $netsendfile_id line] >=0} {
	lappend netsend_list $line
    }
}
######################################################
# Proc - generate net send messages.
######################################################
proc netsend {net_message} {

    global netsend_list    

    foreach name $netsend_list {
        puts "exec net send $name $net_message."
        exec net send $name $net_message
    }
}
########################################################
# Proc - get user roles from input file and process into list
#      - note that there can be several users to a role so "list user"
########################################################
proc get_userroles {userrolesfileid} {

   puts "executing get_userroles"

   global list_userroleslist
 
   puts "User roles are ...................."
   puts ""

   while {[gets $userrolesfileid line] >=0} {
       puts "role mapping is: $line"
       lappend roleslist $line 
   }
#   puts "roleslist = $roleslist"
   set list_userroleslist [list $roleslist]
#   puts "list_userroleslist = $list_userroleslist"
}
########################################################
# Proc - get group roles from input file and process into list
#      - note that there can be several group to a role so "list group"
########################################################
proc get_grouproles {grouprolesfileid} {

   puts "executing get_grouproles"

   global list_grouproleslist
 
   puts "Group roles are ...................."
   puts ""


   while {[gets $grouprolesfileid line] >=0} {
       puts "group role mapping is: $line"
       lappend grouproleslist $line 
   }
   set list_grouproleslist [list $grouproleslist]
}
########################################################
# Proc - get virtual host mappings
#      - note vhosts can be spread across nodes
########################################################
proc get_vhosts {vhostsfileid} {

   puts "executing get_vhosts"

   global list_vhostlist
 
   set block [read -nonewline $vhostsfileid]
   
   puts "virtual host mappings are ................"
   puts ""

   foreach {module vhost} $block {
       puts "vhost mapping = $module $vhost"
        lappend vhostlist [list $module $vhost] 
   }
   
   set list_vhostlist $vhostlist

}
########################################################
# Proc - get appserver mappings
#      - note webmodules can be spread across appservers
########################################################
proc get_servers {serverfileid} {

   puts "executing get_servers"

   global list_serverlist
 
   set block [read -nonewline $serverfileid]
   
   puts "appserver mappings are ................"
   puts ""

   foreach {module server} $block {
       puts "server mapping = $module $server"
        lappend serverlist [list $module $server] 
   }
   set list_serverlist $serverlist
   
}
######################################################
# Proc - create enterprose app.
######################################################
proc create_enterprise_app {nodeId earFile appName defAppServer netSendMsg list_userroleslist list_grouproleslist list_vhostlist list_serverlist} {

    puts "EnterpriseApp install $nodeId  "
    puts "			$earFile "
#    puts "	                -defAppServer $defAppServer"  
    puts "                      -moduleappservers $list_serverlist" 
    puts "			-appname $appName "
    puts "                      -modvirtualhosts $list_vhostlist" 
    puts "			-userroles $list_userroleslist" 
    puts "			-grouproles $list_grouproleslist" 

    puts "########################################"
    puts "Creating $appName Enterprise Application"
    puts "########################################"


    if {[catch { 
	        EnterpriseApp install $nodeId \
	                              $earFile \
				      -appname $appName                  \
                                      -moduleappservers $list_serverlist \ 
				      -modvirtualhosts $list_vhostlist   \
				      -userroles $list_userroleslist     \
				      -grouproles $list_grouproleslist   \
		} result_var] == 0} {
	puts $result_var
	puts "${defAppServer} deployed sucessfully"
       } else {
	       puts $result_var
	       puts "########################################"
	       puts "${defAppServer} failed to deploy"
	       puts "########################################"
	       netsend $netSendMsg
    }
}
######################################
# Control block"
######################################

check_args $argc 

assign_param $argv

puts ""

check_file $netSendFile    $netSendMsg
check_file $earFile        $netSendMsg
check_file $userrolesFile  $netSendMsg
check_file $grouprolesFile $netSendMsg
check_file $vhostsfile     $netSendMsg
check_file $serverfile     $netSendMsg

puts ""

set netSendFile_id    [open $netSendFile r]
set userrolesFile_id  [open $userrolesFile   r]
set grouprolesFile_id [open $grouprolesFile   r]
set vhostsfileid      [open $vhostsfile  r]
set serverfileid      [open $serverfile  r]

get_netsend  $netSendFile_id 

puts ""

get_userroles $userrolesFile_id

puts ""

get_grouproles $grouprolesFile_id

puts ""

get_vhosts $vhostsfileid

get_servers $serverfileid

puts ""

puts "create_enterprise_app"

create_enterprise_app $nodeId $earFile $appName $defAppServer $netSendMsg $list_userroleslist $list_grouproleslist $list_vhostlist $list_serverlist

######################################
# Close files
######################################

close $netSendFile_id
close $userrolesFile_id
close $grouprolesFile_id
close $vhostsfileid 

######################################
# END
######################################
