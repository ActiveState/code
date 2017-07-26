#!/usr/bin/python
import time
import sys
from impacket import ImpactPacket
from socket import *


if len(sys.argv) < 3:
	print """"Usage: <source IP> <dest IP> "data" """
	sys.exit(1)
	
src = sys.argv[1]
dst = sys.argv[2]
str = sys.argv[3]

# define RAW socket
s = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

# define IP packet
ip = ImpactPacket.IP()
ip.set_ip_src(src)
ip.set_ip_dst(dst)

# define ICMP packet
icmp = ImpactPacket.ICMP()
icmp.set_icmp_type(icmp.ICMP_ECHOREPLY) #ICMP packet type

# fragmentation for DATA fileds > of 54 bytes
x = len(str) / 54								 
y = len(str) % 54								 

seq_id = 0										
for i in range(1,x+2):							 
	str_send = str[54*(i-1): 54*i]				 
	icmp.contains(ImpactPacket.Data(str_send)) # fill ICMP DATA field
	ip.contains(icmp) # encapsulate ICMP packet in the IP packet	 
	seq_id = seq_id + 1							 
	icmp.set_icmp_id(seq_id)					 
	icmp.set_icmp_cksum(0)						 
	icmp.auto_checksum = 1						 
	s.sendto(ip.get_packet(), (dst, 0)) # send packet		 
	time.sleep(1)								 
# eventual rest of the string 
str_send = str[54*i:54*i+ y]
icmp.contains(ImpactPacket.Data(str_send))
ip.contains(icmp)
seq_id = seq_id + 1
icmp.set_icmp_id(seq_id)
icmp.set_icmp_cksum(0)
icmp.auto_checksum = 1
s.sendto(ip.get_packet(), (dst, 0))
time.sleep(1)
