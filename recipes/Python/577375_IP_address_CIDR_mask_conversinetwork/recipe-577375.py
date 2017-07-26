def ip_d2a(ipdec):
	ip1 = (ipdec >> 24) & 255;
	ip2 = (ipdec >> 16) & 255;
	ip3 = (ipdec >> 8)  & 255;
	ip4 =  ipdec       & 255;
	
	return "%d.%d.%d.%d" % (ip1, ip2, ip3, ip4);
#

def ipToNetAndHost(ip_str, mask_cidr):
	"returns tuple ((network_itn, network_str), (broadcast_int, broadcast_str))"
	
	l = ip_str.split('.');
	for i in range( len(l) ):	l[i] = int(l[i]);
	
	ip_int = (l[0] << 24) + (l[1] << 16) + (l[2] << 8) + l[3];
	mask_int = (~0 << (32 - mask_cidr));
	net_int = (ip_int & mask_int);
	net_str = ip_d2a(net_int); #print "(DBG) network: [%s] [%d]" % (net_str, net_int);
	brdcast_int = (net_int | ~(mask_int));
	brdcast_str = ip_d2a(brdcast_int); #print "(DBG) broadcast: [%s] [%d]" % (brdcast_str, brdcast_int);
	
	return ((net_int, net_str), (brdcast_int, brdcast_str));
#

"""
import random

subNetList = ['10.0.2.0/23']
subNetList_2 = [];

for s in subNetList:
	l = s.split('/');
	t = ipToNetAndHost(l[0], int(l[1]));
	subNetList_2.append(t);
#

subNetList_2_Size = len(subNetList_2) - 1;

while <...>:
        l = "....".split("....");
        
        # Changes srcAddr AND dstAddr
	t = subNetList_2[ random.randint(0, subNetList_2_Size) ];
	l[1] = random.randint(t[0][0] + 1, t[1][0] - 1);  #excludes network and broadcast
	
	l[2] = random.randint(t[0][0] + 1, t[1][0] - 1);
	while(l[2] == l[1]): l[2] = random.randint(t[0][0] + 1, t[1][0] - 1);
	
	l[1] = ip_d2a(l[1]);
	l[2] = ip_d2a(l[2]);

"""
