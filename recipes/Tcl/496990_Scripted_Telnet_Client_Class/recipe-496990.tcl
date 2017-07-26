package require Itcl 3.3
package require telnet 2.0.0

itcl::class TelnetClient {
    public variable host ""
    public variable port 23
    public variable user "admin"
    public variable password "password"
    public variable timeout 10
    public variable debug 0
    private variable my_sock ""

    private variable out_buffer ""
    public variable xwait ""
    common xtimeout 
    
    constructor {args} {}
    destructor {
        disconnect
    }
    
    public method connect {args}
    public method send {args}
    public method disconnect {}
    private method get_data {}
    private method wait_complete {}
    private method timeout {}
    private method reset_timeout {}
    private method wait_or_timeout {}
}

# Lowercase access procedure
proc telnetclient {args} {
    uplevel ::TelnetClient $args
}

itcl::body TelnetClient::constructor {args} {
    eval configure $args
    
    if {($ip == "") || ($port == "")} {
        error "IP and Port must be specified"
    }
}

itcl::body TelnetClient::connect {args} {
    if {![catch {telnet::open $host $port} conn]} {
        set my_sock $conn
        fconfigure $my_sock -blocking false -buffering none -translation auto -eofchar {}
        flush $my_sock
        fileevent $my_sock readable [itcl::code $this get_data]
        wait_or_timeout
        if {[regexp -nocase {(username|login|user)\s?:} $out_buffer]} {
            set login [send "$user"]
            if {[regexp -nocase {(password)\s?:} $login]} {
                set passdRes [send "$password"]
                if {[regexp {(.>)} $passdRes]} {
                    return 0
                } else {
                    close $conn
                    error "Error: Unexpected System Prompt"
                }
            } else {
                close $conn
                error "Error: Unexpectd Password Prompt"
            }
        } else {
            close $conn
            error "Error: Unexpected Login Prompt"
        }
        
    } else {
        error "Error: Connection Refused"
    }
}

itcl::body TelnetClient::get_data {} {
    if {[eof $my_sock]} {
        close $my_sock
        set connected 0
    } else {
        if {![catch {telnet::read  $my_sock} data]} {
            switch -regexp $data {
                # Add login and password patterns as needed
                {([Uu]sername|[Ll]ogin|[Pp]assword)\s?:} {
                    append out_buffer $data
                    wait_complete
                    return
                }
                # Change this value to your Telnet Prompt
                {.>} {
                    append out_buffer $data
                    wait_complete
                    return
                }
                default {
                    append out_buffer $data
                    reset_timeout
                }
            }
        } else {
            wait_complete
            close $mySocked
            return
        }
    }
}

itcl::body TelnetClient::timeout {} {
    catch {after cancel $xwait}
    set xtimeout($this) 1
    puts "Timeout of after [expr {$timeout * 1000}] seconds"
    return
}

itcl::body TelnetClient::wait_or_timeout {} {
    set xwait [after [expr {$timeout * 1000}] [itcl::code $this timeout]]
    vwait [itcl::scope xtimeout($this)]
    return
}

itcl::body tti::TelnetClient::reset_timeout {} {
    catch {after cancel $xwait}
    set xwait [after [expr {$timeout * 1000}] [itcl::code $this timeout]]
    return
}
itcl::body TelnetClient::wait_complete {} {
    catch {after cancel $xwait} wres
    set xtimeout($this) 1
    return
}

itcl::body TelnetClient::send {data} {
    
    set out_buffer ""
    if {![eof $my_sock]} {
        if {![catch {telnet::write $my_sock "$data\r"} err]} {
            flush $my_sock
            fileevent $my_sock readable [itcl::code $this get_data]
            wait_or_timeout
            return $out_buffer
        } else {
            error "$err"
        }
    } else {
        error "Error: Connection Closed"
    }

}

itcl::body TelnetClient::disconnect {} {
    catch { close $my_sock }
}
