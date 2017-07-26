use warnings;
use strict;
use Net::Syslog;

my $syslog=Net::Syslog->(
    Facility    =>  'local4',
    Priority    =>  'debug',
    SyslogHost  =>  '192.168.1.1'
  );

$syslog->send( 'Message to be sent to remote syslog server' , Priority => 'info');
