import weblog.combined, sys, time, math

def getTimeslice(period, utime):
    low = int(math.floor(utime)) - period + 1
    high = int(math.ceil(utime)) + 1
    for x in range(low, high):
        if x % period == 0:
            return x

def main(files):
    START = time.mktime([2001,11,12,9,0,0,0,0,0])
    END   = time.mktime([2001,11,12,10,0,0,0,0,0])
    t = 0
    slices = {}
    for file in files:
        print file
        log = weblog.combined.Parser(open(file))
        i = 0
        while log.getlogent():
            if log.utime<START or log.utime>END: continue
            slice = getTimeslice(60, log.utime)
            if slices.get(slice) is None:
                slices[slice] = 1
            else:
                slices[slice]=slices[slice]+1
            i=i+1
        print i
        t = t + i

    avg = None
    peak = 0
    peak_ts = 0
    for ts in slices.keys():
        if avg is None:
            avg = slices[ts]
        else:
            avg = (avg + slices[ts]) / 2
        if slices[ts] > peak:
            peak = slices[ts]
            peak_ts = ts
        
    print "Total: %s" % t
    print "Average: %s" % avg
    print "Peak: %s (at %s seconds)" % (peak, peak_ts)

if __name__ == '__main__':
    files = sys.argv[1:]
    main(files)
