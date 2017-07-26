#!/usr/bin/env python

from chm.chm import CHMFile
from os.path import basename, exists, abspath
from HTMLParser import HTMLParser
from sys import argv, exit, stderr
import re

class LinksLocator(HTMLParser):
    """
    LinksLocator is a class for retrieve name and path (Name and Local)
    from TopicsTree in chm (compresed html) archive file or simple
    html links
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_obj = False
        self.nodes = []
        self.in_a = False
        self.links = []

    def handle_starttag(self, tag, attr):
        if tag == 'object':
            self.in_obj = True
            self.new_node = {}
        elif tag == 'param' and self.in_obj:
            attr = dict(attr)
            name = attr['name']
            if name in ('Name', 'Local'):
                self.new_node[name] = attr['value']
        elif tag == 'a':
            attr = dict(attr)
            self.in_a = True
            self.lnk = {'Local': attr.get('href')}
            self.data = ''

    def handle_endtag(self, tag):
        if tag == 'object':
            self.in_obj = False
            if self.new_node != {}:
                self.nodes.append(self.new_node)
        elif tag == 'a':
            self.in_a = False
            # if link has an adress
            if self.lnk.get('Local'):
                self.lnk['Name'] = self.data
                self.links.append(self.lnk)
    def handle_data(self, data):
        if self.in_a:
            self.data += data

class ChmFileException(Exception): pass

class SimpleChmFile(CHMFile):
    """
    SimpleChmFile is a wraper over CHMFile in witch you can iterate over
    pages eg.:

    >>> chm = SimpleChmFile('file.chm')
    >>> for page in chm:
    ...     print page

    the output will be html content of compresed chm file
    """
    def __init__(self, filename=None):
        CHMFile.__init__(self)
        self.nodes = []
        if filename:
            self.open(filename)

    def __iter__(self):
        """return generator over pages in Content Tree."""
        for node in self.nodes:
            yield self._get_contents(node['Local'])

    def open(self, filename):
        if CHMFile.LoadCHM(self, filename) != 1:
            raise IOError, "Can't load File '%s'" % filename
        self.nodes = self._get_nodes()
        if not self.nodes:
            raise ChmFileException, "Can't find Content Tree"

    def _get_contents(self, path):
        """return html contents of file `path' in chm archive."""
        obj = CHMFile.ResolveObject(self, path)
        if obj[0] != 0:
            return None
        html = CHMFile.RetrieveObject(self, obj[1])
        return html[1]

    def _get_nodes(self):
        """return list of dictionaries with data extracted from TopicsTree."""
        parser = LinksLocator()
        home_dir = self.home[:self.home.rfind('/')+1]
        tree = CHMFile.GetTopicsTree(self)
        if tree:
            parser.feed(tree)
            nodes = parser.nodes
        else:
            # try to locate Table of Contents
            obj = self._get_contents(self.home)
            if not obj:
                raise ChmFileException, "Can't find Content Tree"
            parser.feed(obj)
            # sometimes the first page of archive contains link to its
            # Content Tree
            regx = re.compile('Content|toc', re.IGNORECASE)
            for obj in parser.links:
                local, name = obj['Local'], obj['Name']
                if regx.search(local) or regx.search(name):
                    obj = self._get_contents(home_dir + local)
                    parser.feed(obj)
                    break
            nodes = parser.links
        parser.close()
        # fix absolute path if nessesery
        for obj in nodes:
            if obj['Local'][0] != '/':
                obj['Local'] = home_dir + obj['Local']
        return nodes


def usage():
    """print usage on stderr."""
    filename = basename(argv[0])
    # don't brake unix pipe, send usege to stderr
    stderr.write('usage:\n\t%s <chm filename>\n\non Unix you can use pipe to c'
                 'onvert chm to ascii\n\t%s foo.chm | lynx -dump -stdin > foo.'
                 'txt\nor\n\t%s foo.chm | html2text -style pretty | foo.txt\ny'
                 'ou can also save the output as commepresed gzip file\n\t%s f'
                 'oo.chm | html2text -style pretty | gzip | foo.gz\nand read i'
                 't with zless:\n\tzless foo.gz\n' % ((filename,)* 4))

def main():
    try:
        if len(argv) == 2:
            chm = SimpleChmFile(argv[1])
            for page in chm:
                print page
        else:
            usage()
    except (ChmFileException, IOError), e:
        print >> stderr, "%s\n" % e
        usage()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
