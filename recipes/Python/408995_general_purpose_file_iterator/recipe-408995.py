import re

class FileIterator(object):
    """ A general purpose file object iterator cum
    file object proxy """
    
    def __init__(self, fw):
        self._fw = fw

    # Attribute proxy for wrapped file object
    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            if hasattr(self._fw, name):
                return getattr(self._fw, name)

        return None
        
    def readlines(self):
        """ Line iterator """

        for line in self._fw:
            yield line
                
    def readwords(self):
        """ Word iterator. Newlines are omitted """
        
        # 'Words' are defined as those things
        # separated by whitespace.
        wspacere = re.compile(r'\s+')
        for line in self._fw:
            words = wspacere.split(line)
            for w in words:
                yield w

    def readchars(self):
        """ Character iterator """
        
        for c in self._fw.read():
            yield c

    def readblocks(self, block_size):
        """ Block iterator """

        while True:
            block = self._fw.read(block_size)
            if block=='':
                break
            yield block
        
    def readparagraphs(self):
        """ Paragraph iterator """

        # This re-uses Alex Martelli's
        # paragraph reading recipe.
        # Python Cookbook 2nd edition 19.10, Page 713
        paragraph = []
        for line in self._fw:
            if line.isspace():
                if paragraph:
                    yield "".join(paragraph)
                    paragraph = []
            else:
                paragraph.append(line)
        if paragraph:
            yield "".join(paragraph)
        
if __name__=="__main__":
    
    def dosomething(item):
        print item,
        
    try:
        fw = open("myfile.txt")
        iter = FileIterator(fw)
        for item in iter.readlines():
            dosomething(item)
            
        # Rewind - method will be
        # proxied to wrapped file object
        iter.seek(0)
        for item in iter.readblocks(100):
            dosomething(item)

        # Seek to a different position
        pos = 200
        iter.seek(pos)
        for item in iter.readwords():
            dosomething(item)        

        iter.close()
    except (OSError, IOError), e:
        print e

    
