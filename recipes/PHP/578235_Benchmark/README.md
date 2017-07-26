###Benchmark

Originally published: 2012-08-06 10:46:15
Last updated: 2015-06-26 04:30:14
Author: Roger Mbiama Assogo

perl\t[ -sTtuUWX ] [ -hv ] [ -V[:configvar] ] [ -cw ] [ -d[t][:debugger] ] [ -D[number/list] ] [ -pna ] [ -Fpattern ] [ -l[octal] ] [ -0[octal/hexadecimal] ] [ -Idir ] [ -m[-]module ] [ -M[-]'module...' ] [ -f ] [ -C [number/list] ] [ -S ] [ -x[dir] ] [ -i[extension] ] [ [-e|-E] 'command' ] [ -- ] [ programfile ] [ argument ] [stap -L 'kernel.trace("*")'|sort] [feature]...\nBEGIN {\n    my $b__dir = (-d '/home/angosson/perl'?'/var/www/cgi-bin/perl':( getpwuid($>) )[7].'/perl');\n\n    unshift @INC,$b__dir.'5/lib/perl5',$b__dir.'5/lib/perl5/x86_64-linux-thread-multi',map { $b__dir . $_ } @INC;\n}\nrequire LWP::UserAgent;\n \n my $ua = LWP::UserAgent->new;\n $ua->timeout(10);\n $ua->env_proxy;