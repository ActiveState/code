import xml.sax

class simpleHandler (xml.sax.ContentHandler):
    """A simple handler that provides us with indices of marked up content."""
    def __init__ (self):        
        self.elements = [] #this will contain a list of elements and their start/end indices
        self.open_elements = [] #this holds info on open elements while we wait for their close
        self.content = ""

    def startElement (self,name,attrs):
        if name=='foobar': return # we require an outer wrapper, which we promptly ignore.
        self.open_elements.append({'name':name,
                                   'attrs':attrs.copy(),
                                   'start':len(self.content),
                                   })

    def endElement (self, name):
        if name=='foobar': return # we require an outer wrapper, which we promptly ignore.
        for i in range(len(self.open_elements)):
            e = self.open_elements[i]
            if e['name']==name:
                # append a  (start,end), name, attrs
                self.elements.append(((e['start'], #start position
                                       len(self.content)),# current (end) position
                                      e['name'],e['attrs'])
                                     )
                del self.open_elements[i]
                return

    def characters (self, chunk):
        self.content += chunk

class MarkupString (str):
    """A simple class for dealing with marked up strings. When we are sliced, we return
    valid marked up strings, preserving markup."""
    def __init__ (self, string):        
        str.__init__(self,string)
        self.handler = simpleHandler()
        xml.sax.parseString("<foobar>%s</foobar>"%string,self.handler)
        self.raw=self.handler.content

    def __getitem__ (self, n):
        return self.__getslice__(n,n+1)

    def __getslice__ (self, s, e):
        # only include relevant elements
        if not e or e > len(self.raw): e = len(self.raw)
        elements = filter(lambda tp: (tp[0][1] >= s and # end after the start...
                                      tp[0][0] <= e # and start before the end
                                      ),
                          self.handler.elements)
        ends = {}
        starts = {}
        for el in elements:
            # cycle through elements that effect our slice and keep track of
            # where their start and end tags should go.
            pos = el[0]
            name = el[1]
            attrs = el[2]
            # write our start tag <stag att="val"...>
            stag = "<%s"%name
            for k,v in attrs.items(): stag += " %s=%s"%(k,xml.sax.saxutils.quoteattr(v))
            stag += ">"
            etag = "</%s>"%name # simple end tag
            spos = pos[0]
            epos = pos[1]
            if spos < s: spos=s
            if epos > e: epos=e
            if epos != spos: # we don't care about tags that don't markup any text
                if not starts.has_key(spos): starts[spos]=[]
                starts[spos].append(stag)
                if not ends.has_key(epos): ends[epos]=[]
                ends[epos].append(etag)
        outbuf = "" # our actual output string
        for pos in range(s,e): # we move through positions
            char = self.raw[pos]
            if ends.has_key(pos):  # if there are endtags to insert...
                for et in ends[pos]: outbuf += et
            if starts.has_key(pos): # if there are start tags to insert
                mystarts = starts[pos]
                # reverse these so the order works out,e.g. <i><b><u></u></b></i>
                mystarts.reverse()
                for st in mystarts: outbuf += st
            outbuf += char
        if ends.has_key(e):
            for et in ends[e]: outbuf+= et
        return MarkupString(str(outbuf)) # the str call is necessary to avoid unicode messiness
