#Python Version 2.1
#
#
#we need the following module

import httplib

# request the page
def GetUrl(ServerAdr,PagePath):
    http = httplib.HTTP(ServerAdr)
    http.putrequest('GET', PagePath)
    http.putheader('Accept', 'text/html')  
    http.putheader('Accept', 'text/plain')  
    http.endheaders()
    httpcode, httpmsg, headers = http.getreply()  
    if httpcode != 200:
      raise "Could not get document: Check URL and Path."   
    doc = http.getfile()
    data = doc.read()  # read file
    doc.close()
    return data


#parse the page and return the part between the start and end token
def ExtractData(in_string, start_line, end_line): 
    lstr=in_string.splitlines() #split
    j=0 #set counter to zero                                    
    for i in lstr:
        j=j+1
        if i.strip() == start_line: slice_start=j #find slice start
        elif i.strip() == end_line: slice_end=j #find slice end
    return lstr[slice_start:slice_end] #return slice



#handle the returned stuff and generate a new page
def main():
    # parameter and constants
    ServerAdr='www.heise.de'
    PagePath='/'
    StartLine='<!-- MITTE (NEWS) -->'
    EndLine='<!-- MITTE (NEWS-UEBERBLICK) -->'
    Head1='<html><head><base href="http://'
    Head2='"></head><body>'
    Foot='</body></html>'

    # call functions
    RawData=GetUrl(ServerAdr, PagePath)
    v=ExtractData(RawData, StartLine, EndLine)    
    #
    # return result and construct page
    print Head1.strip()+ServerAdr.strip()+Head2.strip()
    for i in v:
        print i.strip() 
    print Foot.strip()


#call main function
main() 
