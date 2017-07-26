#!/usr/bin/env python

from xml import dom
from xml.dom.xmlbuilder import DOMInputSource, DOMBuilder
import datetime
import time
import os

def group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
    
    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.
    
    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)]) 

def remove_whilespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text decendants of a DOM node.
    
    When creating a DOM from an XML source, XML parsers are required to
    consider several conditions when deciding whether to include
    whitespace-only text nodes. This function ignores all of those
    conditions and removes all whitespace-only text decendants of the
    specified node. If the unlink flag is specified, the removed text
    nodes are unlinked so that their storage can be reclaimed. If the
    specified node is a whitespace-only text node then it is left
    unmodified."""
    
    remove_list = []
    for child in node.childNodes:
        if child.nodeType == dom.Node.TEXT_NODE and \
           not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whilespace_nodes(child)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()

class POpenInputSource(DOMInputSource):
    "Use stdout from a system command as a DOMInputSource"
    def __init__(self, command):
        super(DOMInputSource, self).__init__()
        
        self.byteStream = os.popen(command)

class OSXSystemProfiler(object):
    "Provide information from the Mac OS X System Profiler"

    def __init__(self, detail=-1):
        """detail can range from -2 to +1, with larger numbers returning more
        information. Beware of +1, it can take several minutes for
        system_profiler to generate the data."""
        b = DOMBuilder()
        self.document = b.parse(
            POpenInputSource('system_profiler -xml -detailLevel %d' % detail))
        remove_whilespace_nodes(self.document, True)

    def _content(self, node):
        "Get the text node content of an element or an empty string"
        if node.firstChild:
            return node.firstChild.nodeValue
        else:
            return ''
    
    def _convert_value_node(self, node):
        """Convert a 'value' node (i.e. anything but 'key') into a Python data
        structure"""
        if node.tagName == 'string':
            return self._content(node)
        elif node.tagName == 'integer':
            return int(self._content(node))
        elif node.tagName == 'real':
            return float(self._content(node))
        elif node.tagName == 'date': #  <date>2004-07-05T13:29:29Z</date>
            return datetime.datetime(
                *time.strptime(self._content(node), '%Y-%m-%dT%H:%M:%SZ')[:5])
        elif node.tagName == 'array':
            return [self._convert_value_node(n) for n in node.childNodes]
        elif node.tagName == 'dict':
            return dict([(self._content(n), self._convert_value_node(m))
                for n, m in group(node.childNodes, 2)])
        else:
            raise ValueError(node.tagName)
    
    def __getitem__(self, key):
        from xml import xpath
        
        # pyxml xpath does not support /element1[...]/element2
        nodes = xpath.Evaluate(
            '//dict[key=%r]' % key, self.document)
        
        results = []
        for node in nodes:
            v = self._convert_value_node(node)[key]
            if isinstance(v, dict) and v.has_key('_order'):
                # this is just information for display
                pass
            else:
                results.append(v)
        return results
    
    def all(self):
        """Return the complete information from the system profiler
        as a Python data structure"""
        
        return self._convert_value_node(
            self.document.documentElement.firstChild)

def main():
    from optparse import OptionParser
    from pprint import pprint

    info = OSXSystemProfiler()
    parser = OptionParser()
    parser.add_option("-f", "--field", action="store", dest="field",
                      help="display the value of the specified field")
    
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("no arguments are allowed")
    
    if options.field is not None:
        pprint(info[options.field])
    else:
        # just print some comment keys known to exist in only one important
        # dictionary
        for k in ['cpu_type', 'current_processor_speed', 'l2_cache_size',
                  'physical_memory', 'user_name', 'os_version', 'ip_address']:
            print '%s: %s' % (k, info[k][0])
        
if __name__ == '__main__':
    main()
