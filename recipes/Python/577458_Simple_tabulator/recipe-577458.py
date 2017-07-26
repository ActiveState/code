import sys
import optparse

DEF_FSEPARATOR = " "
DEF_LWIDTH = 80
DEF_HEADER = ""
DEF_FOOTER = ""
DEF_LSEPARATOR = "\n"

def main(lwidth,fseparator,lseparator,header,footer):
    try:
        line = []
        llen = 0
        lensep = len(fseparator)
        print header
        for i in sys.stdin:
            i = i.strip()
            llen += len(i) + lensep
            if llen <= lwidth:
                line.append(i)
            else:
                print fseparator.join(line) + fseparator + lseparator,
                line = []
                llen = 0
    except KeyboardInterrupt:
        None
        
    print footer
    
def parse_options():
    parser = optparse.OptionParser(usage="%prog [options] [file]", version="%prog 0.1")
    parser.add_option("-s","--fseparator",action="store",type="string",dest="fseparator",default = DEF_FSEPARATOR,
                      help="String used to separate fields. Defaults to '%s'"%DEF_FSEPARATOR)
    parser.add_option("-w","--width",action="store",type="int",dest="width", default = DEF_LWIDTH,
                      help="Maximum width of the table in characters. Defaults to '%d'"%DEF_LWIDTH)
    parser.add_option("-H","--header",action="store",type="string",dest="header", default = DEF_HEADER,
                      help="Header to be printed before tabulated output. Defaults to '%s'"%DEF_HEADER)
    parser.add_option("-F","--footer",action="store",type="string",dest="footer", default = DEF_FOOTER,
                      help="Footer to be printed after tabulated output. Defaults to '%s'"%DEF_FOOTER)
    parser.add_option("-l","--lseparator",action="store",type="string",dest="lseparator", default = DEF_LSEPARATOR,
                      help=r"String used to separate lines. Defaults to '%s'"%DEF_LSEPARATOR)
    foo = parser.parse_args()
    return foo

if __name__ == "__main__":
    options,args = parse_options()
    main(options.width,
         options.fseparator,
         options.lseparator,
         options.header,
         options.footer
         )
