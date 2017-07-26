#!/usr/bin/env python
"""
        prints, based on input:
                current day
                previous day
                next day

        barbour
        29-Sep-2011
"""
import sys
import datetime

lsarg=len(sys.argv)
funcs={"previous":-1, "current":0, "next":1}

def yj2dt(y,jd):
        return datetime.datetime.strptime("%04i %03i"%(y,jd),"%Y %j")

def ymd2dt(y,m,md):
        return datetime.datetime.strptime("%04i %02i %02i"%(y,m,md),"%Y %m %d")

def dt2yj(dt):
        return dt.strftime("%Y %j")

def dt2ymd(dt):
        return dt.strftime("%Y %m %d")

def dayIter(base, daydelta):
        return base + datetime.timedelta(days = daydelta)

if __name__ == "__main__" and len(sys.argv)==1:
        print """
        usage:  func    year    day
        or      func    year    month   day

        'func' may be
                %s

        output will be the same as input (e.g. year julian, or year month day)
        """ % funcs.keys()

elif __name__ == "__main__" and lsarg > 1:

        fcn = str(sys.argv[1])

        try:
                deld = funcs[fcn]
        except KeyError:
                print "allowable functions:\n%s\n"%funcs.keys()
                raise

        if lsarg == 4:
                # year julian
                yy = int(sys.argv[2])
                jj = int(sys.argv[3])
                print dt2yj( dayIter( yj2dt(yy, jj), deld) )
        elif lsarg == 5:
                # year month day
                yy = int(sys.argv[2])
                mm = int(sys.argv[3])
                dd = int(sys.argv[4])
                print dt2ymd( dayIter( ymd2dt(yy, mm, dd), deld) )
