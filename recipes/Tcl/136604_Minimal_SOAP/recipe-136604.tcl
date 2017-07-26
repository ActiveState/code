% package require SOAP
1.6
% SOAP::create c2f -uri http://www.soaplite.com/Temperature \
      -proxy http://services.soaplite.com/temper.cgi \
      -params { "temp" "float" }
::c2f
% c2f -40.0
24.8
