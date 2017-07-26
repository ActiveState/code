echo off

echo ****************************************
echo * stop WSAPP Enterprise App on %COMPUTERNAME%
echo ****************************************

setlocal

set ENTAPP=/EnterpriseApp:WSAPP/

call wscp -p c:\scripts\websphere\wscp_properties.txt ^
          -f c:\scripts\tcl\stop_ent_app.tcl ^
          -- %ENTAPP%

endlocal

---------------------------------------------------

if {$argc < 0} {
        error "no arguments"
        puts "no arguments"
}

set entApp [lindex $argv 0]

puts "stopping Enterprise App $entApp"

puts "EnterpriseApp stop $entApp"

if {[catch {EnterpriseApp stop $entApp} result_var] ==0}  {
       puts $result_var
       puts "$entApp stopped sucessfully"
   } else {  
	   puts $result_var
	   error "$entApp failed to stop"
   }
   
set status [EnterpriseApp show $entApp -attribute {Name CurrentState}]

puts "status = $status" 
