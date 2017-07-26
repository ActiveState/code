"""Finds a windows hostname given the username
NB. At the time of writing there is a problem in netbios.py 
that in FIND_NAME_BUFFER_ITEMS was missing a comma between field and value
causing a too few items to unpack error
"""
import sys
import netbios
import socket

NetBiosErrorMap = {
    netbios.NRC_BUFLEN 	: "An illegal buffer length was supplied.",
    netbios.NRC_ILLCMD 	: "An illegal command was supplied.",
    netbios.NRC_CMDTMO 	: "The command was timed out.",
    netbios.NRC_INCOMP 	: "The message was incomplete. The application is to issue another command.",
    netbios.NRC_BADDR 	: "The buffer address was illegal.",
    netbios.NRC_SNUMOUT : "The session number was out of range.",
    netbios.NRC_NORES 	: "No resource was available.",
    netbios.NRC_SCLOSED : "The session was closed.",
    netbios.NRC_CMDCAN 	: "The command was canceled.",
    netbios.NRC_DUPNAME : "A duplicate name existed in the local name table.",
    netbios.NRC_NAMTFUL : "The name table was full.",
    netbios.NRC_ACTSES 	: "The command finished; the name has active sessions and is no longer registered.",
    netbios.NRC_LOCTFUL : "The local session table was full.",
    netbios.NRC_REMTFUL : "The remote session table was full. The request to open a session was rejected.",
    netbios.NRC_ILLNN 	: "An illegal name number was specified.",
    netbios.NRC_NOCALL 	: "The system did not find the name that was called.",
    netbios.NRC_NOWILD 	: "Wildcards are not permitted in the ncb_name member.",
    netbios.NRC_INUSE 	: "The name was already in use on the remote adapter.",
    netbios.NRC_NAMERR 	: "The name was deleted.",
    netbios.NRC_SABORT 	: "The session ended abnormally.",
    netbios.NRC_NAMCONF : "A name conflict was detected.",
    netbios.NRC_IFBUSY 	: "The interface was busy.",
    netbios.NRC_TOOMANY : "Too many commands were outstanding; the application can retry the command later.",
    netbios.NRC_BRIDGE 	: "The ncb_lana_num member did not specify a valid network number.",
    netbios.NRC_CANOCCR : "The command finished while a cancel operation was occurring.",
    netbios.NRC_CANCEL 	: "The NCBCANCEL command was not valid; the command was not canceled.",
    netbios.NRC_DUPENV 	: "The name was defined by another local process.",
    netbios.NRC_ENVNOTDEF 	: "The environment was not defined. A reset command must be issued.",
    netbios.NRC_OSRESNOTAV 	: "Operating system resources were exhausted. The application can retry the command later.",
    netbios.NRC_MAXAPPS 	: "The maximum number of applications was exceeded.",
    netbios.NRC_NOSAPS 	: "No service access points (SAPs) were available for NetBIOS.",
    netbios.NRC_NORESOURCES : "The requested resources were not available.",
    netbios.NRC_INVADDRESS 	: "The NCB address was not valid. This return code is not part of the IBM NetBIOS 3.0 specification and is not returned in the NCB structure. Instead, it is returned by Netbios.",
    netbios.NRC_INVDDID : "The NCB DDID was invalid.",
    netbios.NRC_LOCKFAIL    : "The attempt to lock the user area failed.",
    netbios.NRC_OPENERR 	: "An error occurred during an open operation being performed by the device driver. This error code is not part of the NetBIOS 3.0 specification.",
    netbios.NRC_SYSTEM 	: "A system error occurred.",
    netbios.NRC_PENDING : "An asynchronous operation is not yet finished."
}

def FIND_HEADER_BUFFER():
    return netbios.NCBStruct(netbios.FIND_NAME_HEADER_ITEMS+netbios.FIND_NAME_BUFFER_ITEMS)

def convertIP(name):
    return ".".join([str(ord(i)) for i in name if ord(i)])

def getHostname(ipaddress):
    return socket.getfqdn(ipaddress).split(".")[0].lower()

def getUserMachine(netbiosname,type=3):
    ncb = netbios.NCB()
    
    # find a lana number to be used 
    ncb.Command = netbios.NCBENUM
    ncb.Buffer = la_enum = netbios.LANA_ENUM()
    rc = netbios.Netbios(ncb)
    if rc != 0: raise RuntimeError, "Netbios lan enum error. " + NetBiosErrorMap[rc]
    lanaNo = ord(la_enum.lana[0]) # using first number found always
    
    # perform a netbios reset, dont know why but must be done!
    ncb.Reset()
    ncb.Command = netbios.NCBRESET
    ncb.Lana_num = lanaNo
    rc = netbios.Netbios(ncb)
    if rc != 0: raise RuntimeError, "Netbios reset error. " + NetBiosErrorMap[rc]
    
    # perform a netbios name query to find the username  
    name = netbiosname.upper().ljust(15) + chr(type)
    ncb.Callname = name
    ncb.Lana_num = lanaNo    
    ncb.Command = netbios.NCBFINDNAME
    ncb.Buffer = adapter = FIND_HEADER_BUFFER()
    rc = netbios.Netbios(ncb)
    if rc != 0: raise RuntimeError, "Netbios findname error. " + NetBiosErrorMap[rc]
    return getHostname(convertIP(adapter.destination_addr))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Requires username"
        print "Useage: %s username" % sys.argv[0]
        sys.exit(1)
    else:
        print "Netbios Name:",sys.argv[1]
        print "Netbios Query type:",3
        print "Hostname:",getUserMachine(sys.argv[1])
