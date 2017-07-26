use warnings;
use strict;
use Win32::OLE('in');
use constant wbemFlagReturnImmediately  => 0x10;
use constant wbemFlagForwardOnly        => 0x20;

getHotfixes(".");

sub getHotfixes {
  my $computer = shift;
  my $objWMIService = Win32::OLE->GetObject("winmgmts:\\\\$computer\\root\\CIMV2") or die "WMI connection failed.\n";
  my $colItems = $objWMIService->ExecQuery("SELECT * FROM Win32_QuickFixEngineering","WQL",wbemFlagReturnImmediately | wbemFlagForwardOnly);

  foreach my $objItem (in $colItems){
    print "$objItem->{HotFixID}," unless ($objItem->{HotFixID}=~/File 1/);
    #print "Name: $objItem->{Name}\n";
    #print "Description: $objItem->{Description}\n";
    #print "Caption: $objItem->{Caption}\n";
    #print "CS Name: $objItem->{CSName}\n";
    #print "Fix Comments: $objItem->{FixComments}\n";
    #print "Install Date: $objItem->{InstallDate}\n";
    #print "Installed By: $objItem->{InstalledBy}\n";
    #print "Installed On: $objItem->{InstalledOn}\n";
    #print "Service Pack In Effect: $objItem->{ServicePackInEffect}\n";
    #print "Status: $objItem->{Status}\n";
    #print "\n";
  }
}
