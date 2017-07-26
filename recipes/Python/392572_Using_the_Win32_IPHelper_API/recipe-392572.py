# openPorts.py

import ctypes
import socket
import struct

def getOpenPorts():
    """
        This function will return a list of ports (TCP/UDP) that the current 
        machine is listening on. It's basically a replacement for parsing 
        netstat output but also serves as a good example for using the 
        IP Helper API:
        http://msdn.microsoft.com/library/default.asp?url=/library/en-
        us/iphlp/iphlp/ip_helper_start_page.asp.
        I also used the following post as a guide myself (in case it's useful 
        to anyone):
        http://aspn.activestate.com/ASPN/Mail/Message/ctypes-users/1966295
   
     """
    portList = []
           
    DWORD = ctypes.c_ulong
    NO_ERROR = 0
    NULL = ""
    bOrder = 0
    
    # define some MIB constants used to identify the state of a TCP port
    MIB_TCP_STATE_CLOSED = 1
    MIB_TCP_STATE_LISTEN = 2
    MIB_TCP_STATE_SYN_SENT = 3
    MIB_TCP_STATE_SYN_RCVD = 4
    MIB_TCP_STATE_ESTAB = 5
    MIB_TCP_STATE_FIN_WAIT1 = 6
    MIB_TCP_STATE_FIN_WAIT2 = 7
    MIB_TCP_STATE_CLOSE_WAIT = 8
    MIB_TCP_STATE_CLOSING = 9
    MIB_TCP_STATE_LAST_ACK = 10
    MIB_TCP_STATE_TIME_WAIT = 11
    MIB_TCP_STATE_DELETE_TCB = 12
    
    ANY_SIZE = 1         
    
    # defing our MIB row structures
    class MIB_TCPROW(ctypes.Structure):
        _fields_ = [('dwState', DWORD),
                    ('dwLocalAddr', DWORD),
                    ('dwLocalPort', DWORD),
                    ('dwRemoteAddr', DWORD),
                    ('dwRemotePort', DWORD)]
    
    class MIB_UDPROW(ctypes.Structure):
        _fields_ = [('dwLocalAddr', DWORD),
                    ('dwLocalPort', DWORD)]
  
    dwSize = DWORD(0)
    
    # call once to get dwSize 
    ctypes.windll.iphlpapi.GetTcpTable(NULL, ctypes.byref(dwSize), bOrder)
    
    # ANY_SIZE is used out of convention (to be like MS docs); even setting this
    # to dwSize will likely be much larger than actually necessary but much 
    # more efficient that just declaring ANY_SIZE = 65500.
    # (in C we would use malloc to allocate memory for the *table pointer and 
    #  then have ANY_SIZE set to 1 in the structure definition)
    
    ANY_SIZE = dwSize.value
    
    class MIB_TCPTABLE(ctypes.Structure):
        _fields_ = [('dwNumEntries', DWORD),
                    ('table', MIB_TCPROW * ANY_SIZE)]
    
    tcpTable = MIB_TCPTABLE()
    tcpTable.dwNumEntries = 0 # define as 0 for our loops sake

    # now make the call to GetTcpTable to get the data
    if (ctypes.windll.iphlpapi.GetTcpTable(ctypes.byref(tcpTable), 
        ctypes.byref(dwSize), bOrder) == NO_ERROR):
      
        maxNum = tcpTable.dwNumEntries
        placeHolder = 0
        
        # loop through every connection
        while placeHolder < maxNum:
        
            item = tcpTable.table[placeHolder]
            placeHolder += 1
            
            # format the data we need (there is more data if it is useful - 
            #    see structure definition)
            lPort = item.dwLocalPort
            lPort = socket.ntohs(lPort)
            lAddr = item.dwLocalAddr
            lAddr = socket.inet_ntoa(struct.pack('L', lAddr))
            portState = item.dwState
                    
            # only record TCP ports where we're listening on our external 
            #    (or all) connections
            if str(lAddr) != "127.0.0.1" and portState == MIB_TCP_STATE_LISTEN:
                portList.append(str(lPort) + "/TCP")
    
    else:
        print "Error occurred when trying to get TCP Table"

    dwSize = DWORD(0)
    
    # call once to get dwSize
    ctypes.windll.iphlpapi.GetUdpTable(NULL, ctypes.byref(dwSize), bOrder)
    
    ANY_SIZE = dwSize.value # again, used out of convention 
    #                            (see notes in TCP section)
    
    class MIB_UDPTABLE(ctypes.Structure):
        _fields_ = [('dwNumEntries', DWORD),
                    ('table', MIB_UDPROW * ANY_SIZE)]  
                    
    udpTable = MIB_UDPTABLE()
    udpTable.dwNumEntries = 0 # define as 0 for our loops sake
    
    # now make the call to GetUdpTable to get the data
    if (ctypes.windll.iphlpapi.GetUdpTable(ctypes.byref(udpTable), 
        ctypes.byref(dwSize), bOrder) == NO_ERROR):
    
        maxNum = udpTable.dwNumEntries
        placeHolder = 0
        while placeHolder < maxNum:

            item = udpTable.table[placeHolder]
            placeHolder += 1
            lPort = item.dwLocalPort
    
            lPort = socket.ntohs(lPort)
            lAddr = item.dwLocalAddr
            
            lAddr = socket.inet_ntoa(struct.pack('L', lAddr))
            
            # only record UDP ports where we're listening on our external 
            #    (or all) connections
            if str(lAddr) != "127.0.0.1":
                portList.append(str(lPort) + "/UDP")
    else:
        print "Error occurred when trying to get UDP Table"
    
    portList.sort()  
    
    return portList

ListofOpenPorts = getOpenPorts()
