import re
import sys

def help():
    print sys.argv[0]+" generates reverse DNS zonefiles for a given subnet."
    print "Usage "+sys.argv[0]+" [ipblock]"
    print "Example: "+sys.argv[0]+" 10.0.0.0/10"

if len(sys.argv) is not 2:
    help()
    sys.exit(1)

subnet = sys.argv[1]

subnet_checker = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}')
n_grps = re.compile(r'\d{1,3}')

is_subnet = subnet_checker.match(subnet)
if not is_subnet:
    help()
    sys.exit(1)

groups = n_grps.findall(subnet)
hbits = int(groups[(len(groups) - 1)])

if hbits < 8:
    help()
    sys.exit(1)
elif hbits > 32:
    help()
    sys.exit(1)

def bit2dec(bit):
    btable = {1:1, 2:2, 3:4, 4:8, 5:16, 6:32, 7:64, 8:128}
    dec = 0
    for x in range(bit):
        dec += btable[x+1]         
    return int(dec)

if __name__ == "__main__":
    bits = 32 - hbits
    hbits16 = int(groups[(len(groups) - 1)])
    if bits <= 8:
        zonefile = open(groups[0]+'.'+groups[1]+'.'+groups[2]+'.db', 'w')
        for x in range(int(groups[3]),(int(groups[3])+bit2dec(bits))):
            rdns = str(x)+'.'+ groups[2]+'.'+groups[1]+'.'+groups[0]+'.'+'IN-ADDR.ARPA\n'
            zonefile.write(rdns)
        zonefile.close()
    elif bits <= 16:
        for x in range(int(groups[2]), bit2dec(bits - 8)):
            zonefile = open(groups[0]+'.'+groups[1]+'.'+str(x)+'.db', 'w')
            for y in range(1, 256):
                rdns = str(y)+'.'+str(x)+'.'+groups[1]+'.'+groups[0]+'.'+'IN-ADDR.ARPA\n'
                zonefile.write(rdns)
            zonefile.close()
    elif bits <= 24:
        for x in range(int(groups[1]), bit2dec(bits - 16)):
            for y in range(1, 256):
                zonefile = open(groups[0]+'.'+str(x)+'.'+str(y)+'.db', 'w')
                for z in range(1, 256):
                    rdns = str(z)+'.'+str(y)+'.'+str(x)+'.'+groups[0]+'.'+'IN-ADDR.ARPA\n'
                    zonefile.write(rdns)
                zonefile.close()
