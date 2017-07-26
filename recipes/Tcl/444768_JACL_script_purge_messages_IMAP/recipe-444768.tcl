#!/bin/env jaclsh
set mailhost mymailserver.lan
set username cyrus
set password "*******"

package require java

java::import java.util.Properties
java::import javax.mail.Folder

set props [java::new Properties]
$props put mail.debug true
set ses [java::call javax.mail.Session getInstance $props]
set store [$ses getStore imap]
$store connect $mailhost $username $password

set delFlag [java::field {javax.mail.Flags$Flag} DELETED]
set cal [java::call java.util.Calendar getInstance]
$cal add [java::field java.util.Calendar DAY_OF_MONTH] -1
set yesterday [$cal getTime]
unset cal

set folderArr [[$store getDefaultFolder] list "user.*.Trash"]
for {set fi 0} {$fi < [$folderArr length]} {incr fi} {
    set f [java::cast com.sun.mail.imap.IMAPFolder [$folderArr get $fi]]
    set acls [$f getACL]
    if {[$acls length] < 2} {
        if {![info exists cyracl]} {
            set cyracl [java::new com.sun.mail.imap.ACL $username \
                    [[$acls get 0] getRights] ]
        }
        $f addACL $cyracl
    }
    $f open [java::field Folder READ_WRITE]
    puts "Folder: [$f getFullName]: [$f getMessageCount] messages"
    for {set mi 1} {$mi <= [$f getMessageCount]} {incr mi} {
        set msg [$f getMessage $mi]
        if {[$yesterday compareTo [$msg getReceivedDate]] >= 0} {
            puts "OLD MSG:"
            puts "- Subject: [$msg getSubject]"
            puts "- Received: [[$msg getReceivedDate] toString]"
            $msg setFlag $delFlag true
            puts "- Now marked as deleted."
        }
    }
    $f close true
    puts "... Expunged folder [$f getFullName]"
    unset f
}
