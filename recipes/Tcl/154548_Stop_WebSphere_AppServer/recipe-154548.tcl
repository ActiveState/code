echo off

:: call tcl script to stop WebSphere App Servers

echo ****************************************
echo * stop servers
echo ****************************************

call wscp -p c:\scripts\websphere\wscp_properties.txt ^
          -f c:\scripts\tcl\stopservers.tcl


---------------------------------------------------------------

stopservers.tcl

# 
# stop servers
#

source c:\\SCRIPTS\\tcl\\showserverstatus.tcl

foreach server [ApplicationServer  list] {

        puts "\n******* stop SERVER $server\n"
        catch {ApplicationServer stop $server}	
}

showServerStatus
