from HTMLParser import HTMLParser

class IdParser(HTMLParser):
    ''' Parses HTML and places any elements with an ID attribute in a
    dictionary for later access... '''

    stacks = dict()
    elements = dict()
    idd = dict()

    def updatepos(self, i, j):
        # overridden to keep track of our pos
        # line number / offset doesn't help too much
        self.abspos = i #can contain ws
        self.abspos2 = j #element starts here
        if i >= j:
            return j
        rawdata = self.rawdata
        nlines = rawdata.count("\n", i, j)
        if nlines:
            self.lineno = self.lineno + nlines
            pos = rawdata.rindex("\n", i, j)
            self.offset = j-(pos+1)
        else:
            self.offset = self.offset + j-i
        return j

    def handle_starttag(self, tag, attrs, desired='id'):
        ''' Change desired to something other than 'id'
            to get other unique elements. '''

        end = self.abspos2 + len(self.get_starttag_text())

        if not self.stacks.has_key(tag):
            self.stacks[tag] = [end]
        else:
            self.stacks[tag].append(end)

        for key, value in attrs:
            if key == desired:
                self.elements[end] = value

    def handle_endtag(self, tag):
        ''' Pop an element from the desired stack and
            extract the data. '''

        o = self.stacks[tag].pop()
        if self.elements.has_key(o):
            self.idd[self.elements[o]] = self.rawdata[o:self.abspos]
