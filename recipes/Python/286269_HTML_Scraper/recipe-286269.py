#06-09-04
#v1.3.0 

# scraper.py
# A general HTML 'parser' and a specific example that will modify URLs in tags.

# Copyright Michael Foord
# You are free to modify, use and relicense this code.
# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html

import re

#namefind is supposed to match a tag name and attributes into groups 1 and 2 respectively.
#the original version of this pattern:
# namefind = re.compile(r'(\S*)\s*(.+)', re.DOTALL)
#insists that there must be attributes and if necessary will steal the last character
#of the tag name to make it so. this is annoying, so let us try:
namefind = re.compile(r'(\S+)\s*(.*)', re.DOTALL)

attrfind = re.compile(
    r'\s*([a-zA-Z_][-:.a-zA-Z_0-9]*)(\s*=\s*'
    r'(\'[^\']*\'|"[^"]*"|[-a-zA-Z0-9./,:;+*%?!&$\(\)_#=~\'"@]*))?')            # this is taken from sgmllib

class Scraper:
    def __init__(self):
        """Initialise a parser."""
        self.buffer = ''
        self.outfile = ''

    def reset(self):
        """This method clears the input buffer and the output buffer."""
        self.buffer = ''
        self.outfile = ''

    def push(self):
        """This returns all currently processed data and empties the output buffer."""
        data = self.outfile
        self.outfile = ''
        return data

    def close(self):
        """Returns any unprocessed data (without processing it) and resets the parser.
        Should be used after all the data has been handled using feed and then collected with push.
        This returns any trailing data that can't be processed.

        If you are processing everything in one go you can safely use this method to return everything.
        """
        data = self.push() + self.buffer
        self.buffer = ''
        return data

    def feed(self, data):
        """Pass more data into the parser.
        As much as possible is processed - but nothing is returned from this method.
        """
        self.index = -1
        self.tempindex = 0
        self.buffer = self.buffer + data
        outlist = []
        thischunk = []
        while self.index < len(self.buffer)-1:          # rewrite with a list of all the occurences of '<' and jump between them, much faster than character by character - which is fast enough to be fair...
            self.index += 1
            inchar = self.buffer[self.index]
            if inchar == '<':
                outlist.append(self.pdata(''.join(thischunk)))
                thischunk = []
                result = self.tagstart()
                if result: outlist.append(result)
                if self.tempindex: break
            else:
                thischunk.append(inchar) 
        if self.tempindex:
            self.buffer = self.buffer[self.tempindex:]
        else:
            self.buffer = ''
            if thischunk: self.buffer = ''.join(thischunk)
        self.outfile = self.outfile + ''.join(outlist)

    def tagstart(self):
        """We have reached the start of a tag.
        self.buffer is the data
        self.index is the point we have reached.
        This function should extract the tag name and all attributes - and then handle them !."""
        test1 = self.buffer.find('>', self.index+1)
        test2 = self.buffer.find('<', self.index+1)         # will only happen for broken tags with a missing '>'
        test1 += 1
        test2 += 1
        if not test2 and not test1:                     
            self.tempindex = self.index                  # if we get this far the buffer is incomplete (the tag doesn't close yet)
            self.index = len(self.buffer)               # this signals to feed that some of the buffer needs saving
            return
        if test1 and test2:
            test = min(test1, test2)
            if test == test2:           # if the closing tag is missing and we're working from the next starting tag - we eed to be careful with our index position...
                mod=1
            else:
                mod=0
        else:
            test = test1 or test2
            if test2:
                mod=1
            else:
                mod=0
        thetag = self.buffer[self.index+1:test-1].strip()

        if thetag.startswith('!'):               # is a declaration or comment
            return self.pdecl()
        if thetag.startswith('?'):
            return self.ppi()                              # is a processing instruction 

        if mod:                   # as soon as we return, the index will have 1 added to it straight away
            self.index = test -2
        else:
            self.index = test -1
            
        if thetag.startswith('/'):
            return self.endtag(thetag)              # is an endtag 

        nt = namefind.match(thetag)
        if not nt: return self.emptytag(thetag)                              # nothing inside the tag ?
        name, attributes = nt.group(1,2)

        matchlist = attrfind.findall(attributes)
        attrs = []
        #the doc says a tag must be nameless to be "empty" so kill
        #next line that calls any tag with no attributes "empty"
        #if not matchlist: return self.emptytag(thetag)                              # nothing inside the tag ?
        for entry in matchlist:
            attrname, rest, attrvalue = entry               # this little chunk nicked from sgmllib - except findall is used to match all the attributes
            if not rest:
                attrvalue = attrname
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                 attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
            attrs.append((attrname.lower(), attrvalue))
        return self.handletag(name.lower(), attrs, thetag)              # deal with what we've found.

################################################################################################
    # The following methods are called to handle the various HTML elements.
    # They are intended to be overridden in subclasses.

    def pdata(self, inchunk):
        """Called when we encounter a new tag. All the unprocessed data since the last tag is passed to this method.
        Dummy method to override. Just returns the data unchanged."""
        return inchunk

    def pdecl(self):
        """Called when we encounter the *start* of a declaration or comment. <!....
        It uses self.index and isn't passed anything.
        Dummy method to override. Just returns."""
        return '<'
    
    def ppi(self):
        """Called when we encounter the *start* of a processing instruction. <?....
        It uses self.index and isn't passed anything.
        Dummy method to override. Just returns."""
        return '<'

    def endtag(self, thetag):
        """Called when we encounter a close tag. </....
        It is passed the tag contents (including leading '/') and just returns it."""
        return '<' + thetag + '>'

    def emptytag(self, thetag):
        """Called when we encounter a tag that we can't extract any valid name or attributes from.
        It is passed the tag contents and just returns it."""
        return '<' + thetag + '>'  

    def handletag(self, name, attrs, thetag):
        """Called when we encounter a tag.
        Is passed the tag name and a list of (attrname, attrvalue) - and the original tag contents as a string."""
        return '<' + thetag + '>'



#################################################################
# The simple test script looks for a file called 'index.html'
# It parses it, and saves it back out as 'index2.html'
#
# See how all the parsed file can safely be returned using the close method.
# If Scraper works - the new file should be a pretty much unchanged copy of the first.

if __name__ == '__main__':
#    a = approxScraper('http://www.pythonware.com/daily', 'approx.py')
    a = Scraper()
    a.feed(open('index.html').read())                   # read and feed
    open('index2.html','w').write(a.close())

#################################################################
    
__doc__ = """
Scraper is a class to parse HTML files.
It contains methods to process the 'data portions' of an HTML and the tags.
These can be overridden to implement your own HTML processing methods in a subclass.
This class does most of what HTMLParser.HTMLParser does - except without choking on bad HTML.
It uses the regular expression and a chunk of logic from sgmllib.py (standard python distribution)

The only badly formed HTML that will cause errors is where a tag is missing the closing '>'. (Unfortunately common)
In this case the tag will be automatically closed at the next '<' - so some data could be incorrectly put inside the tag.

The useful methods of a Scraper instance are :

feed(data)  -   Pass more data into the parser.
                As much as possible is processed - but nothing is returned from this method.  
push()      -   This returns all currently processed data and empties the output buffer.
close()     -   Returns any unprocessed data (without processing it) and resets the parser.
                Should be used after all the data has been handled using feed and then collected with push.
                This returns any trailing data that can't be processed.
reset()     -   This method clears the input buffer and the output buffer.

The following methods are the methods called to handle various parts of an HTML document.
In a normal Scraper instance they do nothing and are intended to be overridden.
Some of them rely on the self.index attribute property of the instance which tells it where in self.buffer we have got to.
Some of them are explicitly passed the tag they are working on - in which case, self.index will be set to the end of the tag.
After all these methods have returned self.index will be incremented to the next character.
If your methods do any future processing they can manually modify self.index
All these methods should return anything to include in the processed document.

pdata(inchunk)
    Called when we encounter a new tag. All the unprocessed data since the last tag is passed to this method.
    Dummy method to override. Just returns the data unchanged.

pdecl()
    Called when we encounter the *start* of a declaration or comment. <!.....
    It uses self.index and isn't passed anything.
    Dummy method to override. Just returns '<'.

ppi()
    Called when we encounter the *start* of a processing instruction. <?.....
    It uses self.index and isn't passed anything.
    Dummy method to override. Just returns '<'.

endtag(thetag)
    Called when we encounter a close tag.   </...
    It is passed the tag contents (including leading '/') and just returns it.

emptytag(thetag)
    Called when we encounter a tag that we can't extract any valid name or attributes from.
    It is passed the tag contents and just returns it.

handletag(name, attrs, thetag)
    Called when we encounter a tag.
    Is passed the tag name and attrs (a list of (attrname, attrvalue) tuples) - and the original tag contents as a string.


Typical usage :

filehandle = open('file.html', 'r')
parser = Scraper()
while True:
    data = filehandle.read(10000)               # read in the data in chunks
    if not data: break                      # we've reached the end of the file - python could do with a do:...while syntax...
    parser.feed(data)
##    print parser.push()                     # you can output data whilst processing using the push method
processedfile = parser.close()              # or all in one go using close  
## print parser.close()                       # Even if using push you will still need a final close
filehandle.close()



TODO/ISSUES
Could be sped up by jumping from '<' to '<' rather than a character by character search (which is still pretty quick).
Need to check I have all the right tags and attributes in the tagdict in approxScraper.
The only other modification this makes to HTML is to close tags that don't have a closing '>'.. theoretically it could close them in the wrog place I suppose....
(This is very bad HTML anyway - but I need to watch for missing content that gets caught like this.)
Could check for character entities and named entities in HTML like HTMLParser.
Doesn't do anything special for self clsoing tags (e.g. <br />)


CHANGELOG
06-09-04        Version 1.3.0
A couple of patches by Paul Perkins - mainly prevents the namefind regular expression grabbing a characters when it has no attributes.

28-07-04        Version 1.2.1
Was losing a bit of data with each new feed. Have sorted it now.

24-07-04        Version 1.2.0
Refactored into Scraper and approxScraper classes.
Is now a general purpose, basic, HTML parser.

19-07-04        Version 1.1.0
Modified to output URLs using the PATH_INFO method - see approx.py
Cleaned up tag handling - it now works properly when there is a missing closing tag (common - but see TODO - has to guess where to close it).

11-07-04        Version 1.0.1
Added the close method.

09-07-04        Version 1.0.0
First version designed to work with approx.py the CGI proxy.

"""
