 ppm
ActivePer-Config
 mkdir -p ~/perl/angosso/
(e.g. set or export)
.bash_profile
PERL5LIB=~/perl/angosso; export PERL5LIB
ppm install Angosso:/tmp/Date-Calc-6.3.ppmx
use ExtUtils::MakeMaker;
  # See lib/ExtUtils/MakeMaker.pm for details of how to influence
  # the contents of the Makefile that is written.
  WriteMakefile(
      'NAME' => 'Term::Control',
      'VERSION_FROM' => 'Control.pm', # finds $VERSION
      ($] ge '5.005') ? (
          'AUTHOR' => 'Roger Mbiama (r.mbiama@angosso.net)',
          'ABSTRACT' => 'Control the IO for terminals',
      ) : (),
  );

  perl Makefile.PL
  nmake
tar cvf package.tar blib
gzip --best package.tar
nmake ppd
http_proxy=http://proxy.example.net
http_proxy=http://username:password@proxy.angosso.net:8080
cpan
install from source
     wget http://www.cpan.org/src/5.0/perl-5.22.0.tar.gz
     tar -xzf perl-5.22.0.tar.gz
     cd perl-5.22.0
     ./Configure -des -Dprefix=$HOME/localperl
     make
     make test
     make install
cpan App::cpanminus
