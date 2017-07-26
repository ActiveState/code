#!/usr/bin/env python
# this is a simple example to sniff on port 80 for magic CAFEBABE. 
# it has to run either sudo root on any Unix or with windows admin right. 
# author email: pythonrocks@gmail.com. 
import dpkt, pcap
import re
import sys

pattern=re.compile('.*CAFEBABE.*')

def __my_handler(ts,pkt,d):


    tcpPkt=dpkt.tcp.TCP(pkt)
    data=tcpPkt.data

    # let's find any java class pass 
    searched=pattern.search(data)

    if searched:
      d['hits']+=1
      print 'counters=',d['hits']

pc = pcap.pcap()
pc.setfilter('tcp and dst port 80')
print 'listening on %s: %s' % (pc.name, pc.filter)
pc.loop(__my_handler)
