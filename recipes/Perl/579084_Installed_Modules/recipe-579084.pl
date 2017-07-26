<!--#include virtual="/directory/included.html" -->
# script to find installed modules
#!/var/www/cgi-bin/perl/bin:perl.exe
use ExtUtils::Installed;

# set the http header as html
print "Content-type: text/html\n\n";

my $inst = ExtUtils::Installed->new();
my @modules = $inst->modules();

print join "<br>", @modules;
