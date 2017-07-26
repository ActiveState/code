import math

class size( long ):
    """ define a size class to allow custom formatting
        Implements a format specifier of S for the size class - which displays a human readable in b, kb, Mb etc 
    """
    def __format__(self, fmt):
        if fmt == "" or fmt[-1] != "S":
            if fmt[-1].tolower() in ['b','c','d','o','x','n','e','f','g','%']:
                # Numeric format.
                return long(self).__format__(fmt)
            else:
                return str(self).__format__(fmt)

        val, s = float(self), ["b ","Kb","Mb","Gb","Tb","Pb"]
        if val<1:
            # Can't take log(0) in any base.
            i,v = 0,0
        else:
            i = int(math.log(val,1024))+1
            v = val / math.pow(1024,i)
            v,i = (v,i) if v > 0.5 else (v*1024,i-1)
        return ("{0:{1}f}"+s[i]).format(v, fmt[:-1])

if __name__ == "__main__":
    # Example usages

    # You can use normal format spcifiers as expected - just use S as the presentation type (instead of f, i etc)
    # and cast the integer byte count to type size.

    # Example format specifications
    print "{0:.1f}".format(4386) # output - 4386.0
    print "{0:.1S}".format(size(4386)) # output 4.3Kb
    print "{0:.2S}".format(size(86247))# output 84.23Kb
