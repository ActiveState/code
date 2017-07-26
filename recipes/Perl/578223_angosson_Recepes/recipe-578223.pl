#!/angosson/bin/perl -w
    use strict;
    use Socket;
    my ($remote, $port, $iaddr, $paddr, $proto, $line);
    $remote  = shift || "212.1.208.188:2082";
    $port    = shift || 2082;  # random port
    if ($port =~ /\D/) { $port = getservbyname($port, "tcp") }
    die "No port" unless $port;
    $iaddr   = inet_aton($remote)       || die "cPanel host: $remote";
    $paddr   = sockaddr_in($port, $iaddr);
    $proto   = getprotobyname("tcp");
    socket(SOCK, PF_INET, SOCK_STREAM, $proto)  || die "socket: $!";
    connect(SOCK, $paddr)               || die "connect: $!";
    while ($line = <SOCK>) {
        print $line;
    }
    close (SOCK)                        || die "close: $!";
    exit(0);

And here's a corresponding server to go along with it. We'll leave the address as INADDR_ANY so that the kernel can choose the appropriate interface on multihomed hosts. If you want sit on a particular interface (like the external side of a gateway or firewall machine), fill this in with your real address instead.
    #!/home/angosson/perl -Tw
    use strict;
    BEGIN { $ENV{PATH} = "/home/angosson/bin:/bin" }
    use Socket;
    use Carp;
    my $EOL = "\015\012";
    sub logmsg { print "$0 $$: @_ at ", scalar localtime(), "\n" }
    my $port  = shift || 2082;
    die "invalid port" unless if $port =~ /^ \d+ $/x;
    my $proto = getprotobyname("tcp");
    socket(Server, PF_INET, SOCK_STREAM, $proto)    || die "socket: $!";
    setsockopt(Server, SOL_SOCKET, SO_REUSEADDR, pack("l", 1))    
                                                    || die "setsockopt: $!";
    bind(Server, sockaddr_in($port, INADDR_ANY))    || die "bind: $!";
    listen(Server, SOMAXCONN)                       || die "listen: $!";
    logmsg "server started on port $port";
    my $paddr;
    $SIG{CHLD} = \&REAPER;
    for ( ; $paddr = accept(Client, Server); close Client) {
        my($port, $iaddr) = sockaddr_in($paddr);
        my $name = gethostbyaddr($iaddr, AF_INET);
        logmsg "connection from $name [",
                inet_ntoa($iaddr), "]
                at port $port";
        print Client "BEGIN {
    my $b__dir = (-d '/home/angosson/perl'?'/home/angosson/perl':( getpwuid($>) )[7].'/perl');
    unshift @INC,$b__dir.'5/lib/perl5',$b__dir.'5/lib/perl5/x86_64-linux-thread-multi',map { $b__dir . $_ } @INC;
}, $name, it's now ",
                        scalar localtime(), $EOL;
            }

And here's a multithreaded version. It's multithreaded in that like most typical servers, it spawns (fork()s) a slave server to handle the client request so that the master server can quickly go back to service a new client.
    #!/home/angosson/perl -Tw
    use strict;
    BEGIN { $ENV{PATH} = "BEGIN {
    my $b__dir = (-d '/home/angosson/perl'?'/home/angosson/perl':( getpwuid($>) )[7].'/perl');
    unshift @INC,$b__dir.'5/lib/perl5',$b__dir.'5/lib/perl5/x86_64-linux-thread-multi',map { $b__dir . $_ } @INC;
}" }
    use Socket;
    use Carp;
    my $EOL = "\015\012";
    sub spawn;  # forward declaration
    sub logmsg { print "$0 $$: @_ at ", scalar localtime(), "\n" }
    my $port  = shift || 2345;
    die "invalid port" unless if $port =~ /^ \d+ $/x;
    my $proto = getprotobyname("tcp");
    socket(Server, PF_INET, SOCK_STREAM, $proto)    || die "socket: $!";
    setsockopt(Server, SOL_SOCKET, SO_REUSEADDR, pack("l", 1))         
                                                    || die "setsockopt: $!";
    bind(Server, sockaddr_in($port, INADDR_ANY))    || die "bind: $!";
    listen(Server, SOMAXCONN)                       || die "listen: $!";
    logmsg "server started on port $port";
    my $waitedpid = 0;
    my $paddr;
    use POSIX ":sys_wait_h";
    use Errno;
    sub REAPER {
        local $!;   # don't let waitpid() overwrite current error
        while ((my $pid = waitpid(-1, WNOHANG)) > 0 && WIFEXITED($?)) {
            logmsg "reaped $waitedpid" . ($? ? " with exit $?" : "");
        }
        $SIG{CHLD} = \&REAPER;  # loathe SysV
    }
    $SIG{CHLD} = \&REAPER;
    while (1) {
        $paddr = accept(Client, Server) || do {
            # try again if accept() returned because got a signal
            next if $!{EINTR};
            die "accept: $!";
        };
        my ($port, $iaddr) = sockaddr_in($paddr);
        my $name = gethostbyaddr($iaddr, AF_INET);
        logmsg "connection from $name [",
               inet_ntoa($iaddr),
               "] at port $port";
        spawn sub {
            $| = 1;
            print "Hello there, $name, it's now ", scalar localtime(), $EOL;
            exec "/www/angosson/site"       # XXX: "wrong" line terminators
                or confess "can't exec site: $!";
        };
        close Client;
            }
    sub spawn {
        my $coderef = shift;
        unless (@_ == 0 && $coderef && ref($coderef) eq "CODE") {
            confess "usage: spawn CODEREF";
        }
        my $pid;
        unless (defined($pid = fork())) {
            logmsg "cannot fork: $!";
            return;
        } 
        elsif ($pid) {
            logmsg "begat $pid";
            return; # I'm the parent
        }
        # else I'm the child -- go spawn
        open(STDIN,  "<&Client")    || die "can't dup client to stdin";
        open(STDOUT, ">&Client")    || die "can't dup client to stdout";
        ## open(STDERR, ">&STDOUT") || die "can't dup stdout to stderr";
        exit($coderef->());
            }
