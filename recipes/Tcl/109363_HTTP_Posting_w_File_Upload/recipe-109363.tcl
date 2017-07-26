#!/bin/sh
# The next line is executed by /bin/sh, but not tcl \
exec tclsh "$0" ${1+"$@"}

##
## httppost.tcl
##
## Post to a web page and return data
##

if {0} {
    ##
    ## EXAMPLES
    ##

    # Uploading a PTS file: (only the file as a Data elem is needed)
    httppost.tcl http://pop/~hobbs/wis/cgi-bin/pq.cgi
	    -user <valid-user> -passwd <users-passwd> \
	    -file Data <PTS_data.txt> var value var value
}

package require Tcl 8.2
package require http 2.2
#package require base64; # from tcllib - only needed for user/passwd
			 # it gets called below when necessary

proc Usage {} {
    puts stderr "[file tail $::argv0] URL \\
	    ?-proxyhost domain? \\
	    ?-proxyport port? \\
	    ?-user user? \\
	    ?-passwd passwd? \\
	    ?-output outputFile? \\
	    ?-file formElemName fileName? \\
	    formElemName value formElemName value ...

    -proxyhost and -proxyport set the proxy to use, if necessary
    -user and -passwd are required if the URL requires authentication

    files are handled specially with -file as the file has to
    be read in and then that is used as the value."
    exit
}

proc process {} {
    global argv

    if {[llength $argv] < 4} {
	Usage
    }
    set opts(URL) [lindex $argv 0]
    set argv [lrange $argv 1 end]

    set opts(FILE) [list]
    while {[string match -* [lindex $argv 0]]} {
	switch -exact -- [lindex $argv 0] {
	    -proxyhost {
		set opts(PROXYHOST) [lindex $argv 1]
		if {![info exists opts(PROXYPORT)]} {
		    set opts(PROXYPORT) 80
		}
		set argv [lrange $argv 2 end]
	    }
	    -proxyport {
		set opts(PROXYPORT) [lindex $argv 1]
		set argv [lrange $argv 2 end]
	    }
	    -user {
		set opts(USER) [lindex $argv 1]
		set argv [lrange $argv 2 end]
	    }
	    -passwd {
		set opts(PASSWD) [lindex $argv 1]
		set argv [lrange $argv 2 end]
	    }
	    -file {
		lappend opts(FILE) [lindex $argv 1] [lindex $argv 2]
		set argv [lrange $argv 3 end]
	    }
	    -output {
		set opts(OUTFILE) [lindex $argv 1]
		set argv [lrange $argv 2 end]
	    }
	    default {
		Usage
	    }
	} 
    }

    if {[info exists opts(PROXYHOST)]} {
	::http::config -proxyhost $opts(PROXYHOST) \
		-proxyport $opts(PROXYPORT)
    }

    ## Configure the output channel
    set outfd stdout
    set type "multipart/form-data"
    if {[info exists opts(OUTFILE)]} {
	set outfd [open $opts(OUTFILE) w]
    }
    fconfigure $outfd -translation binary

    set outputData {}
    set bound "-----NEXT_PART_[clock seconds].[pid]"
    foreach {elem file} $opts(FILE) {
	set fid [open $file r]
	fconfigure $fid -translation binary
	if {[catch {read $fid [file size $file]} data]} {
	    return -code error $data
	}
	close $fid
	append outputData "--$bound\nContent-Disposition: form-data;\
		name=\"$elem\"; filename=\"[file tail $file]\"\n\n$data\n"
    }
    foreach {elem data} $argv {
	append outputData "$bound\nContent-Disposition: form-data;\
		name=\"$elem\"\n\n$data\n"
    }
    if {![string length $outputData]} {
	return -code error "No data given to post"
    }
    append outputData "${bound}--"

    set request [list ::http::geturl $opts(URL) \
	    -channel $outfd \
	    -type "multipart/form-data; boundary=$bound" \
	    -query $outputData]

    if {[info exists opts(USER)] && [info exists opts(PASSWD)]} {
	package require base64
	lappend request -headers [list Authorization \
		"Basic [base64::encode $opts(USER):$opts(PASSWD)]"]
    }

    set token [eval $request]
    ::http::wait $token
    if {[string compare stdout $outfd]} {
	close $outfd
    }
}

process
