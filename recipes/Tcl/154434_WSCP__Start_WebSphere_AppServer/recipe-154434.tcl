echo off

:: call tcl script to start WebSphere App Servers

echo ****************************************
echo * start servers on %computername%
echo ****************************************

call wscp -p c:\scripts\websphere\wscp_properties.txt ^
          -f c:\scripts\tcl\startservers.tcl


-----------------------------------------------------------------------

startservers.tcl

# 
# start WebSphere AppServer
#
source c:\\SCRIPTS\\tcl\\showserverstatus.tcl

foreach server [ApplicationServer  list] {

        puts "\n*******start SERVER $server\n"
        catch {ApplicationServer start $server}	
}

showServerStatus
