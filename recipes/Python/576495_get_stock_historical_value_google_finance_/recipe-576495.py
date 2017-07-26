import urllib2
import re
from table_parser import *


"""
By bussiere bussiere @at gmail.com
thanks to :
http://simbot.wordpress.com/2006/05/17/html-tables-parsed-using-python/
Nigel Sim <nigel.sim @at gmail.com>
http://simbot.wordpress.com

"""

__Author__ ="bussiere"
__Email__ = "bussiere @at gmail.com"
__Titre__ = "get some value with google finance"
__Description__ = "get the historical value on google finance"
__Discussion__ = "A beginnig for a stock analyze program."
__Tags__ ="google fiance stock value historical"

def get_finance(value):
    #we make a url for google finance with the value given
    link = "http://finance.google.com/finance?q=%s"%value
    #we open this url
    page = urllib2.urlopen(link).read()
    #we find where is the hisctorical link
    findhistorical = re.findall("/finance/historical\?q.*\"", page)
    print findhistorical
    #we substract the " at the end of the string
    findhistorical = findhistorical[0].replace('\"','')
    #we make a link for the historical page of the value
    histlink = "http://finance.google.com%s"%findhistorical
    #we open the historical page
    hist = urllib2.urlopen(histlink).read()
    #we find the link for getting the data in csv mode
    findcsv = re.findall('http://finance.*csv',hist)
    #we open the link
    csv = ''
    try :
        #we try to get the csv file if existent
        csv = urllib2.urlopen(findcsv[0]).read()
    except :
        #else we parse the google finance page with table parser
        findcsv = re.findall('<div id=prices>.*?</table>',hist,re.S)
        p = TableParser()
        p.feed(findcsv[0])
        csv = p.doc
    #we return the csv data for the value
    return csv
    
    

def main(argv=None):
    # we get the argument passed on the command line
    value =  sys.argv[1]
    print get_finance(value)








if __name__ == "__main__":
    import sys
    #we call the main function
    sys.exit(main())
