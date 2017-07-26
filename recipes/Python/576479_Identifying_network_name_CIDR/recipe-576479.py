# David.Clark (a) CIBER-research.eu 2012-12-20

# CIBER Research Ltd.
# version 10 hybrid for both clarity and optimisation, + bug fix.
# this code is online at
#       http://code.activestate.com/recipes/576479/

""" Create a digital trie of ipranges(CIDR); for a given ip 
determine membership of smallest CIDR (if any) by digital search. 

    'Instead of basing a search method on comparisons between keys, 
we can make use of their representation as a sequence of digits or
alphabetic characters.'
        Knuth. Art of Computer Programming vol 3, 2e 1998 (6.3 p492)
"""
	
def bytes2bits():
    """Create a table of bit values for int(0) to int(256)."""
    # derived from  Python Cookbook 2e 2005.
    bytes = [None] * 256
    for n in xrange(256):
        bits = []
        q = n                       # q is modified by bitshift
        for b in xrange(0,8):
            if (q & 128):
                bits.append(1)
            else:
                bits.append(0)
            q <<= 1
        bytes[n] = tuple(bits)      # make immutable
    return tuple(bytes)
# One-time call to build table; rebind the funtion name to its result.
bytes2bits = bytes2bits()

class ProgramError(ValueError):
    """This is a bug"""

class CIDRnode(object):
    def __init__(self, cidr=None):
        self.cidr = cidr
        self.left = None
        self.right = None

    def get_net(self):
        if self.cidr:
            return self.cidr.split('/')[0]
        else:
            return None
    network = property(get_net, doc='IPv4 dotted quad')

    def get_bits(self):
        if self.cidr:
            return int(self.cidr.split('/')[1])
        else:
            return None
    netbits = property(get_bits, doc='IPv4 netmask bits')

class CIDRtrie(object):
    """
    take a shortcut by using a list for the first octet as any CIDR 
    will be no greater than class A. Thereafter work down a binary tree
    of ip network addresses. If a node has a CIDR record stack the result,
    but continue down the tree while there are links. (Not all Nodes 
    have CIDR records.). At leif node pop (the best) result.
    """
    # we need some definitions before we can __init__()
    @staticmethod
    def byte2bit(ip):
        for q in ip:
            q = int(q) 
            for b in xrange(0,8):
                yield 1 if (q & 128) else 0
                q <<= 1

    def add_cidr(self, cidr):
        """Build the trie. For clarity this is the non-optimised version."""
        c = cidr.split('/')
        network = c[0].split('.')
        nm_bit = int(c[1])
        classA = int(network[0])
        subtree = self.root[classA] 
        if not subtree:
            subtree = CIDRnode()
            self.root[classA] = subtree
        nm_bit -= 7             # leave a bit for test at top of loop
        network_bits = self.byte2bit(network[1:])
        for nextbit in network_bits: 
            if nm_bit == 1:
                overwrite = subtree.cidr
                subtree.cidr = cidr
                return overwrite                # expect to return None
            nm_bit -= 1        
            if nextbit is 0:
                if not subtree.left:
                    subtree.left = CIDRnode()
                subtree = subtree.left
                continue
            elif nextbit is 1:
                if not subtree.right:
                    subtree.right = CIDRnode()
                subtree = subtree.right
                continue
            else:
                raise ProgramError(
                    'Tried to bud %s, bitten by bug, fell out of Tree'% cidr)
        subtree.cidr = cidr

    def __init__(self, ipranges=None):
        self.root = [None] * 256        # A forest of (x.0.0.0/8) 'class A' addresses
        if ipranges:
            for cidr in ipranges:
                self.add_cidr(cidr)

    def get_cidr(self, ip):
        """This is very similar to add_cidr but inline code improves
        performance by around 10% and the cost of building the lookup table
        is amortised over serveral million lookups gaining another 10%."""
        ip = ip.split('.')
        subtree = self.root[int(ip[0])]         # subtree = CIDRnode
        if subtree is None:
            return None
        results = [None]
        for quad in ip[1:]:
            quad_bits = bytes2bits[int(quad)]
            for nextbit in quad_bits:
                if subtree.cidr:
                    results.append(subtree.cidr)
                if subtree.left and nextbit is 0:
                    subtree = subtree.left
                    continue
                elif subtree.right and nextbit is 1:
                    subtree = subtree.right
                    continue
                else:
                    return results.pop()
        return subtree.cidr

####    Command Line Processing    ####
def test():
    index = {}
    networks = (
        ('10.40.47.0/27', 'network 1'),
        ('10.40.0.0/16' , 'network 2'),
        ('10.44.0.0/16' , 'network 3'),
        ('192.168.47.0/27','network 4'),
        ('10.10.1.1/32' , 'single_ip'),)
    ipaddr = ('10.40.47.26', '10.40.47.34', '10.44.47.26',
            '192.168.47.0', '192.168.47.31', '192.168.47.32',  
            '192.168.0.47', '192.168.47.1', '10.10.1.1')
    trie = CIDRtrie()
    for cidr, name in networks:
        index[cidr] = name
        overwrite = trie.add_cidr(cidr)
        if overwrite:
            print('WARNING overwriting %s with %s'% (overwrite, cidr))

    for ip in ipaddr:
        cidr = trie.get_cidr(ip)
        if cidr:
            name = index[cidr]
            print('%s is in network %s (%s)'% (ip, name, cidr))
        else:
            print('network not known for %s'% ip)

if __name__ == '__main__':     #only when run from cmd line
    test()
