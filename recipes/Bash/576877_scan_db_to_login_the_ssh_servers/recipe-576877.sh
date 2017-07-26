#!/bin/bash

hostname=${1:?"host name?"}
regexp="(.*):(.*):(.*)"

#set the sshdb data to be default if the database is unspecified
default_sshdb="/home/jing/sshserver/sshdb"
sshdb=${2:-$default_sshdb}

#read the host to be connected
account=$(awk -v host=$hostname '
/^[^#].*/ { 
    if ( $1 ~ host ) {
     printf $2 ":"$3 ":"$4
        exit
    }
}
' $sshdb)

if [[ $account =~ $regexp ]];then
    ip=${BASH_REMATCH[1]}
    username=${BASH_REMATCH[2]}
    password=${BASH_REMATCH[3]}
fi

#make the connection
/usr/bin/expect -f /home/jing/sshserver/expectedssh $username $ip $password











==================================================================
jing@jing-laptop:~$ cat sshserver/expectedssh 
set UserID "[lrange $argv 0 0]"
set Passphrase "[lrange $argv 2 2]"
set remotehost "[lrange $argv 1 1]"

set timeout 30

spawn ssh $UserID@$remotehost
expect -re ".*password:"
send "$Passphrase\r"
expect -re ".+"
interact







==================================================================
#this is the database for ssh connection using expect
#connection-name host username password, delimited by a single space

25 172.16.100.25 liujingyuan aaaaa
26 172.16.100.26 liujingyuan aaaaa
106 172.16.100.106 root root12
