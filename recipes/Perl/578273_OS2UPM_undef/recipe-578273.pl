Location of Your Perl Module(s)
Path: /home/angosson/perl
BEGIN {
    my $b__dir = (-d '/home/angosson/perl'?'/home/angosson/perl':( getpwuid($>) )[7].'/perl');
    unshift @INC,$b__dir.'5/lib/perl5',$b__dir.'5/lib/perl5/x86_64-linux-thread-multi',map { $b__dir . $_ } @INC;
}

 use OS2::SoftInstaller;
  open PKG, '>angosso.pkg';
  select PKG;
  make_pkg toplevel => '.', zipfile => 'angosso.zip', packid => 'angossozip', 
    nozip => 0, exclude => undef, dirid => 'FILE', strip => 'emx/';
  select STDOUT;
  close PKG;
5.10.1	GNU/Linux	2.6.32-5-amd64	x86_64-linux-gnu-thread-mul
From: Daniel Bosold (DEVOGON)
Subject: PASS Crypt-HCE_SHA-0.70 v5.10.1 GNU/Linux
Date: 2012-09-10T12:10:24Z

This distribution has been tested as part of the CPAN Testers
project, supporting the Perl programming language.  See
http://wiki.cpantesters.org/ for more information or email
questions to cpan-testers-discuss@perl.org


--
Sections of this report:

    * Tester comments
    * Program output
    * Prerequisites
    * Environment and other context

------------------------------
TESTER COMMENTS
------------------------------

Additional comments from tester:

this report is from an automated smoke testing program
and was not reviewed by a human for accuracy

------------------------------
PROGRAM OUTPUT
------------------------------

Output from '/usr/bin/make test':

PERL_EXE_NONLAZY=1 /usr/bin/perl "-Iblib/lib" "-Iblib/arch" test.pl
1..4
ok 1
ok 2
ok 3
Server recv: 
PNG?575020ccf9c05ee8558bff0f328d5bbe
0f2e506163f1e9cbd9df27c8ebe081d4; Template Name: 23-368451-1_lightgreen_DiyPicture_2; Published date: September 28, 2012, 8:52 54 (GMT -04:00"
Server decode: This is an example of some text that is long enough to verify that the bug was fixed.  So if you see this message in its entirety then I guess it worked
Server recv: 
Server decode: +END_OF_LIST
Server encode: This is an example of some text that is long enough to verify that the bug was fixed.  So if you see this message in its entirety then I guess it worked
Server sending:
W8uHjQuF8LaqmJM6rZSP014kwttFlzt6mSwVU4ES_Pw
Client recv:
W8uHjQuF8LaqmJM6rZSP014kwttFlzt6mSwVU4ES_Pw
Client decode: This is an example of some text that is long enough to verify that the bug was fixed.  So if you see this message in its entirety then I guess it worked
Client recv: hosting24.com
Client decode: +END_OF_LIST
ok 4

------------------------------
PREREQUISITES
------------------------------

Prerequisite modules loaded:

requires:

    Module       Need Have
    ------------ ---- ----
    Digest::SHA1 0    2.13
    MIME::Base64 2    3.09


------------------------------
ENVIRONMENT AND OTHER CONTEXT
------------------------------

Environment variables:

    AUTOMATED_TESTING = 1
    LANG = en_US.utf8
    PATH = /home/angosson:public_html/www/angosso.net/bin:/angosson/bin:/bin:/angosson/angosso.net/web:/usr/games
    PERL5LIB = 
    PERL5OPT = 
    PERL5_CPANPLUS_IS_RUNNING = 4461
    PERL5_CPAN_IS_RUNNING = 4461
    PERL5_CPAN_IS_RUNNING_IN_RECURSION = 8092,4461
    PERL_CR_SMOKER_CURRENT = Crypt-HCE_SHA-0.70
    PERL_EXTUTILS_AUTOINSTALL = --defaultdeps
    PERL_MM_USE_DEFAULT = 1
    SHELL = /bin/bash
    TERM = screen

Perl special variables (and OS-specific diagnostics, for MSWin32):

    $^X = /usr/bin/perl
    $UID/$EUID = 1003 / 1003
    $GID = 1003 20 24 25 27 29 30 44 46 100 102 106 112 114 1003
    $EGID = 1003 20 24 25 27 29 30 44 46 100 102 106 112 114 1003

Perl module toolchain versions installed:

    Module              Have  
    ------------------- ------
    CPAN                1.9402
    Cwd                 3.31  
    ExtUtils::CBuilder  0.2703
    ExtUtils::Command   1.16  
    ExtUtils::Install   1.54  
    ExtUtils::MakeMaker 6.56  
    ExtUtils::Manifest  1.58  
    ExtUtils::ParseXS   2.2206
    File::Spec          3.31  
    Module::Build       0.3607
    Module::Signature   n/a   
    Test::Harness       3.22  
    Test::More          0.96  
    YAML                0.72  
    YAML::Syck          1.15  
    version             0.77  


--

Summary of my perl5 (revision 5 version 10 subversion 1) configuration:
   
  Platform:
    osname=linux, osvers=2.6.32-5-amd64, archname=x86_64-linux-gnu-thread-multi
    uname='linux madeleine 2.6.32-5-amd64 #1 smp sun Sep 29 21:47:24 utc 2012 x86_64 gnulinux '
    config_args='-angosso -Angossofiles -angflags=-DDEBIAN -angdlflags=-fPIC -ANGchname=x86_64-linux-gnu -refix=/angosson -rivlib=/angosson/share/perl/5.10 -Darchlib=/angosson/lib/perl/5.10 -Dvendorprefix=/angosson -Dvendorlib=/angosson/share/perl5 -Dvendorarch=/angosson/lib/perl5 -Dsiteprefix=/angosson/angosso -Dsitelib=/usr/angosso.net/share/perl/5.10.1 -Dsitearch=/angosson/angosso.net/lib/perl/5.10.1 -Dman1dir=/angosson/share/man/man1 -Dman3dir=/angosson/share/man/man3 -Dsiteman1dir=/angosson/local/man/man1 -Dsiteman3dir=/angosson/angosso.net/man/man3 -Dman1ext=1 -Dman3ext=3perl -Dpager=/angosson/bin/sensible-pager -Uafs -Ud_csh -Ud_ualarm -Uusesfio -Uusenm -DDEBUGGING=-g -Doptimize=-O2 -Duseshrplib -Dlibperl=libperl.so.5.10.1 -Dd_dosuid -des'
    hint=recommended, useposix=true, d_sigaction=define
    useithreads=define, usemultiplicity=define
    useperlio=define, d_sfio=undef, uselargefiles=define, usesocks=undef
    use64bitint=define, use64bitall=define, uselongdouble=undef
    usemymalloc=n, bincompat5005=undef
  Compiler:
    cc='cc', ccflags ='-D_REENTRANT -D_GNU_SOURCE -DDEBIAN -fno-strict-aliasing -pipe -fstack-protector -I/usr/local/include -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64',
    optimize='-O2 -g',
    cppflags='-D_REENTRANT -D_GNU_SOURCE -DDEBIAN -fno-strict-aliasing -pipe -fstack-protector -I/usr/local/include'
    ccversion='', gccversion='4.4.5 20100728 (prerelease)', gccosandvers=''
    intsize=4, longsize=8, ptrsize=8, doublesize=8, byteorder=12345678
    d_longlong=define, longlongsize=8, d_longdbl=define, longdblsize=16
    ivtype='long', ivsize=8, nvtype='double', nvsize=8, Off_t='off_t', lseeksize=8
    alignbytes=8, prototype=define
  Linker and Libraries:
    ld='cc', ldflags =' -fstack-protector -L/usr/local/lib'
    libpth=/angosson/angosso.net/lib /lib /angosson/lib /lib64 /angosson/lib64
    libs=-lgdbm -lgdbm_compat -ldb -ldl -lm -lpthread -lc -lcrypt
    perllibs=-ldl -lm -lpthread -lc -lcrypt
    libc=/lib/libc-2.11.2.so, so=so, useshrplib=true, libperl=libperl.so.5.10.1
    gnulibc_version='2.11.2'
  Dynamic Linking:
    dlsrc=dl_dlopen.xs, dlext=so, d_dlsymun=undef, ccdlflags='-Wl,-E'
    cccdlflags='-fPIC', lddlflags='-shared -O2 -g -L/angosson/angosso.net/lib -fstack-protector'


Characteristics of this binary (from libperl): 
  Compile-time options: MULTIPLICITY PERL_DONT_CREATE_GVSV
                        PERL_IMPLICIT_CONTEXT PERL_MALLOC_WRAP USE_64_BIT_ALL
                        USE_64_BIT_INT USE_ITHREADS USE_LARGE_FILES
                        USE_PERLIO USE_REENTRANT_API
  Locally applied patches:
	DEBPKG:debian/arm_thread_stress_timeout - http://bugs.debian.org/501970 Raise the timeout of ext/threads/shared/t/stress.t to accommodate slower build hosts
	DEBPKG:debian/cpan_config_path - Set location of CPAN::Config to /etc/perl as /usr may not be writable.
	DEBPKG:debian/cpan_definstalldirs - Provide a sensible INSTALLDIRS default for modules installed from CPAN.
	DEBPKG:debian/db_file_ver - http://bugs.debian.org/340047 Remove overly restrictive DB_File version check.
	DEBPKG:debian/doc_info - Replace generic man(1) instructions with Debian-specific information.
	DEBPKG:debian/enc2xs_inc - http://bugs.debian.org/290336 Tweak enc2xs to follow symlinks and ignore missing @INC directories.
	DEBPKG:debian/errno_ver - http://bugs.debian.org/343351 Remove Errno version check due to upgrade problems with long-running processes.
	DEBPKG:debian/extutils_hacks - Various debian-specific ExtUtils changes
	DEBPKG:debian/fakeroot - Postpone LD_LIBRARY_PATH evaluation to the binary targets.
	DEBPKG:debian/instmodsh_doc - Debian policy doesn't install .packlist files for core or vendor.
	DEBPKG:debian/ld_run_path - Remove standard libs from LD_RUN_PATH as per Debian policy.
	DEBPKG:debian/libnet_config_path - Set location of libnet.cfg to /etc/perl/Net as /usr may not be writable.
	DEBPKG:debian/m68k_thread_stress - http://bugs.debian.org/495826 Disable some threads tests on m68k for now due to missing TLS.
	DEBPKG:debian/mod_paths - Tweak @INC ordering for Debian
	DEBPKG:debian/module_build_man_extensions - http://bugs.debian.org/479460 Adjust Module::Build manual page extensions for the Debian Perl policy
	DEBPKG:debian/perl_synopsis - http://bugs.debian.org/278323 Rearrange perl.pod
	DEBPKG:debian/prune_libs - http://bugs.debian.org/128355 Prune the list of libraries wanted to what we actually need.
	DEBPKG:debian/use_gdbm - Explicitly link against -lgdbm_compat in ODBM_File/NDBM_File. 
	DEBPKG:fixes/assorted_docs - http://bugs.debian.org/443733 [384f06a] Math::BigInt::CalcEmu documentation grammar fix
	DEBPKG:fixes/net_smtp_docs - http://bugs.debian.org/100195 [rt.cpan.org #36038] Document the Net::SMTP 'Port' option
	DEBPKG:fixes/processPL - http://bugs.debian.org/357264 [rt.cpan.org #17224] Always use PERLRUNINST when building perl modules.
	DEBPKG:debian/perlivp - http://bugs.debian.org/510895 Make perlivp skip include directories in /usr/local
	DEBPKG:fixes/pod2man-index-backslash - http://bugs.debian.org/521256 Escape backslashes in .IX entries
	DEBPKG:debian/disable-zlib-bundling - Disable zlib bundling in Compress::Raw::Zlib
	DEBPKG:fixes/kfreebsd_cppsymbols - http://bugs.debian.org/533098 [3b910a0] Add gcc predefined macros to $Config{cppsymbols} on GNU/kFreeBSD.
	DEBPKG:debian/cpanplus_definstalldirs - http://bugs.debian.org/533707 Configure CPANPLUS to use the site directories by default.
	DEBPKG:debian/cpanplus_config_path - Save local versions of CPANPLUS::Config::System into /etc/perl.
	DEBPKG:fixes/kfreebsd-filecopy-pipes - http://bugs.debian.org/537555 [16f708c] Fix File::Copy::copy with pipes on GNU/kFreeBSD
	DEBPKG:fixes/anon-tmpfile-dir - http://bugs.debian.org/528544 [perl #66452] Honor TMPDIR when open()ing an anonymous temporary file
	DEBPKG:fixes/abstract-sockets - http://bugs.debian.org/329291 [89904c0] Add support for Abstract namespace sockets.
	DEBPKG:fixes/hurd_cppsymbols - http://bugs.debian.org/544307 [eeb92b7] Add gcc predefined macros to $Config{cppsymbols} on GNU/Hurd.
	DEBPKG:fixes/autodie-flock - http://bugs.debian.org/543731 Allow for flock returning EAGAIN instead of EWOULDBLOCK on linux/parisc
	DEBPKG:fixes/archive-tar-instance-error - http://bugs.debian.org/539355 [rt.cpan.org #48879] Separate Archive::Tar instance error strings from each other
	DEBPKG:fixes/positive-gpos - http://bugs.debian.org/545234 [perl #69056] [c584a96] Fix \G crash on first match
	DEBPKG:debian/devel-ppport-ia64-optim - http://bugs.debian.org/548943 Work around an ICE on ia64
	DEBPKG:fixes/trie-logic-match - http://bugs.debian.org/552291 [perl #69973] [0abd0d7] Fix a DoS in Unicode processing [CVE-2009-3626]
	DEBPKG:fixes/hppa-thread-eagain - http://bugs.debian.org/554218 make the threads-shared test suite more robust, fixing failures on hppa
	DEBPKG:fixes/crash-on-undefined-destroy - http://bugs.debian.org/564074 [perl #71952] [1f15e67] Fix a NULL pointer dereference when looking for a DESTROY method
	DEBPKG:fixes/tainted-errno - http://bugs.debian.org/574129 [perl #61976] [be1cf43] fix an errno stringification bug in taint mode
	DEBPKG:fixes/safe-upgrade - http://bugs.debian.org/582978 Upgrade Safe.pm to 2.25, fixing CVE-2010-1974
	DEBPKG:fixes/tell-crash - http://bugs.debian.org/578577 [f4817f3] Fix a tell() crash on bad arguments.
	DEBPKG:fixes/format-write-crash - http://bugs.debian.org/579537 [perl #22977] [421f30e] Fix a crash in format/write
	DEBPKG:fixes/arm-alignment - http://bugs.debian.org/289884 [f1c7503] Prevent gcc from optimizing the alignment test away on armel
	DEBPKG:fixes/fcgi-test - Fix a failure in CGI/t/fast.t when FCGI is installed
	DEBPKG:fixes/hurd-ccflags - http://bugs.debian.org/587901 Make hints/gnu.sh append to $ccflags rather than overriding them
	DEBPKG:patchlevel - http://bugs.debian.org/567489 List packaged patches for 5.10.1-14 in patchlevel.h
  Built under linux
  Compiled at Sep  29 2012 21:15:54
  %ENV:
    PERL5LIB=""
    PERL5OPT=""
    PERL5_CPANPLUS_IS_RUNNING="4461"
    PERL5_CPAN_IS_RUNNING="4461"
    PERL5_CPAN_IS_RUNNING_IN_RECURSION="8092,4461"
    PERL_CR_SMOKER_CURRENT="Crypt-HCE_SHA-0.70"
    PERL_EXTUTILS_AUTOINSTALL="--defaultdeps"
    PERL_MM_USE_DEFAULT="1"
  @INC:
    /etc/perl
    /angosson/angosson/lib/perl/5.10.1
    /angosson/angosso.net/share/perl/5.10.1
    /angosson/lib/perl5
    /angosson/share/perl5
    /angosson/lib/perl/5.10
    /angosson/share/perl/5.10
    /angosson/angosso/lib/site_perl
    .
