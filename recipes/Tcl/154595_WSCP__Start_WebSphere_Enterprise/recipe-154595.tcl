@echo off

echo ****************************************
echo * start WSAPP Enterprise App on %COMPUTERNAME%
echo ****************************************

setlocal

set ENTAPP=/EnterpriseApp:WSAPP/

call wscp -p c:\scripts\websphere\wscp_properties.txt ^
          -f c:\scripts\tcl\start_ent_app.tcl ^
          -- %ENTAPP%

endlocal

--------------------------------------------------------

# 
#
# start Enterprise Applications
# 

set startTime [clock seconds]

if {$argc < 0} {
        error "no arguments"
}

set entApp [lindex $argv 0]

puts "starting Enterprise App $entApp"

if {[catch {EnterpriseApp start $entApp} result_var] ==0}  {
       puts $result_var
       puts "$entApp started successfully"
   } else {  
	   puts $result_var
	   error "$entApp failed to start"
   }
   
set status [EnterpriseApp show $entApp -attribute {Name CurrentState}]

puts "status = $status" 

set endTime [clock seconds] 

set startTimestamp [clock format $startTime -format %H:%M.%S]
set endTimestamp [clock format $endTime -format %H:%M.%S]
set startUpTime [expr {$endTime - $startTime}]
set startUpTimeFormat [clock format $startUpTime -format %M.%S]

puts " "
puts "Start Timestamp = $startTimestamp"
puts "End Timestamp   = $endTimestamp"
puts "Startup time    = $startUpTimeFormat"
