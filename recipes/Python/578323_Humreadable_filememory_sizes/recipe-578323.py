import math
import string

class size( long ):
    """ define a size class to allow custom formatting
        format specifiers supported : 
            em : formats the size as bits in IEC format i.e. 1024 bits (128 bytes) = 1Kib 
            eM : formats the size as Bytes in IEC format i.e. 1024 bytes = 1KiB
            sm : formats the size as bits in SI format i.e. 1000 bits = 1kb
            sM : formats the size as bytes in SI format i.e. 1000 bytes = 1KB
            cm : format the size as bit in the common format i.e. 1024 bits (128 bytes) = 1Kb
            cM : format the size as bytes in the common format i.e. 1024 bytes = 1KB
    """
    def __format__(self, fmt):
        # is it an empty format or not a special format for the size class
        if fmt == "" or fmt[-2:].lower() not in ["em","sm","cm"]:
            if fmt[-1].lower() in ['b','c','d','o','x','n','e','f','g','%']:
                # Numeric format.
                return long(self).__format__(fmt)
            else:
                return str(self).__format__(fmt)

        # work out the scale, suffix and base        
        factor, suffix = (8, "b") if fmt[-1] in string.lowercase else (1,"B")
        base = 1024 if fmt[-2] in ["e","c"] else 1000

        # Add the i for the IEC format
        suffix = "i"+ suffix if fmt[-2] == "e" else suffix

        mult = ["","K","M","G","T","P"]

        val = float(self) * factor
        i = 0 if val < 1 else int(math.log(val, base))+1
        v = val / math.pow(base,i)
        v,i = (v,i) if v > 0.5 else (v*base,i-1)

        # Identify if there is a width and extract it
        width = "" if fmt.find(".") == -1 else fmt[:fmt.index(".")]        
        precis = fmt[:-2] if width == "" else fmt[fmt.index("."):-2]

        # do the precision bit first, so width/alignment works with the suffix
        t = ("{0:{1}f}"+mult[i]+suffix).format(v, precis) 

        return "{0:{1}}".format(t,width) if width != "" else t

if __name__ == "__main__":
    # Example usages

    # You can use normal format spcifiers as expected - just use the correct the presentation type (instead of f, e, G etc)
    # and cast the integer byte count to type size.

    # Example format specifications
    print "{0:.1f}".format(4386) # output - 4386.0
    print "{0:.1f}".format(size(4386)) # output 4386.0 - default numeric presentations respected.
    print "{0:.2eM}".format(size(86247)) # output 84.23KiB - base 1024
    print "{0:.2sM}".format(size(86247)) # output 86.25KB - base 1000
    print "{0:.2cM}".format(size(86247)) # output 84.23KB - base 1024
    print "{0:.2cm}".format(size(86247)) # output 0.66Mb - base 1024 in bits.
