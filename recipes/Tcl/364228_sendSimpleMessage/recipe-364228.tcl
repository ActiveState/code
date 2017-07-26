proc sendSimpleMessage {email_address subject body} {

    puts "\n*** sendSimpleMessage proc ***\n"

    package require smtp
    package require mime

    set emailServer your.email.server

    puts "\nemail address: $email_address"
    puts "subject:       $subject"
    puts "body:          $body"
    puts "email_server:  $emailServer\n"

    set computer_name $::env(COMPUTERNAME)

    set message [mime::initialize -canonical text/plain -file $body]
    
    smtp::sendmessage $message -servers $emailServer \
		               -header [list To $email_address] \
		               -header [list From $computer_name] \
		               -header [list Subject $subject]

    mime::finalize $message
    
}
