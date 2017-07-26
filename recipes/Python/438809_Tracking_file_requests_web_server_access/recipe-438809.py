from operator import itemgetter
from socket import gethostbyaddr, herror
import time

accessLog = "/var/log/apache2/access_log"

def track(filename, logFile=accessLog):
    """Retrieve request statistics for a specific file in an access log."""
    log = open(logFile)
    filename = '/' + filename.lstrip('/')
    access = {}
    for line in log:
        parts = line.split()
        if parts[6] == filename:
            timeStr = parts[3]
            accessTime = time.strptime(timeStr, "[%d/%b/%Y:%H:%M:%S")
            access[parts[0]] = (accessTime, access.get(parts[0], ('', 0))[1] + 1)
    print '%s has been requested by %d people and hit %d times.' % \
          (filename, len(access), sum(map(itemgetter(1), access.itervalues())))
    
    accessTuple = sorted(access.iteritems(), key=itemgetter(1))
    hitWidth = len(str(max([data[1] for user, data in accessTuple])))

    for user, data in accessTuple:
        lastAccess, hits = data
        print 'User: %s Last Access: %s Hits: %s' % \
              ((user+",").ljust(16),
               time.strftime("%a %d-%b-%Y %I:%M:%S %p,", lastAccess),
               str(hits).rjust(hitWidth))

    return accessTuple

def resolve(*args):
    """Resolve a sequence of IP addresses to their hostnames, if possible."""
    if len(args) > 1:
        addrList = args
    else:
        addrList = args[0]
    for addr in addrList:
        if isinstance(addr, tuple):
            addr = addr[0]
        try:
            host = gethostbyaddr(addr)[0]
        except (herror, IndexError):
            host = addr
        print 'Addr: %s Hostname: %s' % ((addr+',').ljust(16), host)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: python track_access.py filename access_log"
    else:
        if len(sys.argv) > 2:
            accessLog = sys.argv[2]
        resolve(track(sys.argv[1], accessLog))
