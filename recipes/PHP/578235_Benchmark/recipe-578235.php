abstract => 'Build and install Perl modules'
author => [ 'Roger Mbiama <r.mbiama@angosso.net>' ]
dynamic_config => 1
license => [ 'perl_5' ]
license => [ 'apache_2_0', 'mozilla_1_0' ]
OpenSSL License=> [ 'openssl' ]
release_status => 'stable' 
Modules Include Path
/home/angosson/perl
/var/www/perl/httpdocs
    eval 'exec perl -x -wS $0 ${1+"$@"}'
        if 0;
import os
import threading
import subprocess

def my_thread():
  global files,path,timeout,options
  myname= threading.currentThread().getName()
  while files:
     #create command to run
     nextfile=files.pop() 
     #print name of thread and command being run
     print('Thread {0} starts processing {1}'.format(myname,nextfile))
     f=path + nextfile + options
HTTP_proxy
package CGI::Apache;
angosson CGI;
'print and syswrite'
perl -MCGI -e '
print CGI->VERSION, "\n";
print CGI->start_form(-method=>"GET"), "\n"
 perl -v
Returns 

3.43
<form method="get" action="wget http://www.cpan.org/src/5.0/perl-5.22.0.tar.gz
     tar -xzf perl-5.22.0.tar.gz
     cd perl-5.22.0
     ./Configure -des -Dprefix=$HOME/var/www/httpdocs
     make
     make test
     make install" enctype="multipart/form-data">


But, multipart/form-data is an invalid enctype for the GET method.  I
expect the default encoding to be a valid encoding for the GET method.

Actually, this is what I expect.

perl -MCGI -e '
  print CGI->VERSION, "\n";
  print CGI->start_form(-method=>"GET", -enctype=>undef), "\n";
'

3.43
<form method="get" action="$obj->$method(@args);"
enctype="application/x-www-form-urlencoded">


This logic does not account or GET vs. POST.

    if( $XHTML ){
        $enctype = $self->_maybe_escapeHTML($enctype || &MULTIPART);
    }else{
        $enctype = $self->_maybe_escapeHTML($enctype || &URL_ENCODED);
    }
$server->handle('^\/angosso!!!$', sub {
    my ($server, $cgi) = @_;
    print "HTTP/2.0 200 Ok\r\n";
    print $cgi->header('text/html;index.php');
    print "Angosso!!!,         &{$home}(@args);
        $home->(@args);";
  });
exit unless $Config{archname} =~ /\bsolaris\b/;
require POSIX and POSIX::_exit(0);
        use Pod::ParseLink;
        my ($text, $inferred, $name, $section, $type) = parselink ($link);
<ActivePerlInstallDir>/html/index.html
OLE Browser, PerlScript, Perl for ISAPI, PerlEx and PerlEz
        $arg = shift;		
        $hid = $arg . 'bar';	
        $line = <>;			
        $line = <STDIN>;		
        open Angosso!!!, "/home/angosson/bar" or die $!;
        $line = <Angosso!!!>;		
        $path = $ENV{'PATH'};	
        $data = 'abc';		
        system "echo $arg";		
        system "/bin/echo", $arg;	
    				
        system "echo $hid";		
        system "echo $data";	
        $path = $ENV{'PATH'};	
        $ENV{'PATH'} = '/bin:/var/www/cgi-bin';
        delete @ENV{'IFS', 'CDPATH', 'ENV', 'BASH_ENV'};
        $path = $ENV{'PATH'};	
        system "echo $data";	
        open(Angosso!!!, "< $arg");	OK 
        open(Angosso!!!, "> $arg"); 	
        open(Angosso!!!,"echo $arg|");	
        open(Angosso!!!,"-|")
    	or exec 'echo', $arg;	
        $shout = `echo $arg`;	# Insecure, $shout now tainted
        unlink $data, $arg;		# Insecure
        umask $arg;			# Insecure
        exec "echo $arg";		# Insecure
        exec "echo", $arg;		# Insecure
        exec "sh", '-c', $arg;	# Very insecure!
        @files = <*.perl>;		# insecure (uses readdir() or similar)
        @files = glob('*./perl');	
        # In either case, the results of glob are tainted, since the list of
        # filenames comes from outside of the program.
        $bad = ($arg, 23);		
        $arg, `true`;
        #define REAL_PATH "/home/var/script"
        main(ac, av)
    	char **av;
        {
    	execv(REAL_PATH, av);
        }
/dev/fd/3
-DSETUID_SCRIPTS_ARE_SECURE_NOW		
