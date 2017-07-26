#  (C) Copyright IBM Corporation, 2000
#  All rights reserved. Licensed Materials Property of IBM 
#  Note to US Government users: Documentation related to restricted rights
#  Use, duplication or disclosure is subject to restrictions set forth 
#  in GSA ADP Schedule with IBM Corp. 
#  This page may contain other proprietary notices and copyright information, 
#  the terms of which must be observed and followed. 

proc showServerStatus {} {
	puts "\nStatus of servers in the domain:\n"
          foreach ejbserver [ApplicationServer list] {
          set serverInfo($ejbserver) [ApplicationServer show $ejbserver -attribute {Name CurrentState}]
          puts $serverInfo($ejbserver)
	
	}
}
