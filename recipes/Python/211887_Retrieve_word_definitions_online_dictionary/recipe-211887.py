"""The following routines are specific to queries to 
www.dictionary.com (as of 2003-07-23)"""

def get_def_page(word):
    """Retrieve the definition page for the word of interest.                                                   
                                                                                                                
    """
    import urllib
    url = "http://www.dictionary.com/cgi-bin/dict.pl?term=%s" % word
    fo = urllib.urlopen(url)
    page = fo.read()
    return page

def get_definitions(wlist):
    """Return a dictionary comprising words (keys) and a definition                                             
    lists (values).                                                                                             
                                                                                                                
    """
    ddict = {}
    for word in wlist:
        text = get_def_page(word)
        defs = extract_defs(text)
        ddict[word] = defs
    return ddict

def extract_defs(text):
    """The site formats its definitions as list items <LI>definition</LI>                                       
                                                                                                                
    We first look for all of the list items and then strip them of any                                          
    remaining tags (like <ul>, <CITE>, etc.). This is done using simple 
    regular expressions, but could probably be done more robustly by
    the method detailed in
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52281                                                                  .
                                                                                                                
    """
    import re

    clean_defs = []
    LI_re = re.compile(r'<LI[^>]*>(.*)</LI>')
    HTML_re = re.compile(r'<[^>]+>\s*')
    defs = LI_re.findall(text)
    # remove internal tags                                                                                      
    for d in defs:
        clean_d = HTML_re.sub('',d)
        if clean_d: clean_defs.append(clean_d)

    return clean_defs


#--------------------------------------------------------------------                                           
#                                                                                                               
#--------------------------------------------------------------------                                           
if __name__ == "__main__":

    defdict = get_definitions(['monty','python','language'])
    print defdict
