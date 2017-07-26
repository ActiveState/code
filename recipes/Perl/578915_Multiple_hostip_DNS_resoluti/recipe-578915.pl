#!/usr/bin/perl
###################################################
# This script will parse a text file containing a
# list of IP Addresses or hostnames (one per line).
#
# Usage: mass_nslookup.pl list_of_hosts.txt
#
###################################################

use warnings;
use strict;
use Net::Nslookup;

open (FILE, $ARGV[0]);

while (<FILE>){
	my $host = $_;
	chomp($host);
	next unless $host;
	resolve_dns($host);
}

close FILE;
sub resolve_dns{
	my $host = shift;
	my $dns = nslookup($host);
	if ($dns){
		print "$host,$dns\n";
	}
}
