package require Expect

exp_log_user 1

set timeout 20
set Machine [lindex $argv 0]
set UserName [lindex $argv 1]
set Password [lindex $argv 2]
set enablePassword [lindex $argv 3]

spawn telnet $Machine

send "$UserName\n"
send "$Password\n"
set enable_logged_in 1
send "en\n"
send "$enablePassword\n"
set logged_in 1

if (!$logged_in) {
    puts "\n Error while logging \n"
    exit
}

puts "\n Hiiiiiiii \n"
