import xml.etree.ElementTree as ET
import re

class ETGen(object):
    TAGSUFFIX = 'XMLTag'
    def __init__(self, xmlin, out, param={}):
        self.counter = 0
        self.constants = {}
        self.lines = []
        
        h = open(xmlin, 'r')
        xml = h.read()
        h.close()
        
        builder = ET.XMLTreeBuilder()
        builder.feed(xml)
        tree = builder.close()
        
        self.out = out
        
        self.__walk(tree, None)
        self.__write()
        
    def __genName(self, name):
        self.counter += 1
        return re.search('(?:{.*?})?(.*)', name).group(1) + ETGen.TAGSUFFIX + str(self.counter)
    
    def __write(self):
        h = open(self.out, 'w')
        h.write("import xml.etree.ElementTree as ET\n\n")
        
        # prints namespace constants
        h.writelines(["%s = '%s'\n" % (v, k) for k, v in self.constants.items()])
        h.write("\n")
        
        h.write("def build(**kwargs):\n\t")
        
        h.write("\n\t".join(self.lines))
        h.write("\n\treturn ET.tostring(%s)\n\n" % self.root)
        
        h.write("if __name__ == '__main__': print build()")
        h.close()
    
    def __getNamespace(self, name):
        ns = re.search('(?:{(.*?)})?(.*)', name).group(1)
        if ns is None:
            return '\'%s\'' % name
        if ns not in self.constants:
            nsName = "NS" + str(len(self.constants))
            self.constants[ns] = nsName
        else:
            nsName = self.constants[ns]
        tag = re.sub('{.*?}(.*)', '\'{%%s}\\1\' %% %s' % nsName, name)
        return tag
        
    def __walk(self, node, parent):
        name = self.__genName(node.tag)        
        tag = self.__getNamespace(node.tag)
              
        if parent is None:
            self.root = name
            self.lines.append("%s = ET.Element(%s)" % (name, tag))
        else:
            self.lines.append("%s = ET.SubElement(%s, %s)" % (name, parent, tag))
            
            # handles text
            try:
                t = node.text.strip()
                if t == '': t = None
            except:
                t = None
                
            if t is not None:
                self.lines.append("%s.text = kwargs.get('', '%s') # PARAMETERIZE" % (name, t))
                
            # handles attributes
            for key,val in node.items():
                key = self.__getNamespace(key)
                self.lines.append("%s.set(%s, kwargs.get('', '%s')) # PARAMETERIZE" % (name, key, val))
        for i in node.getchildren():
            self.__walk(i, name)

def main():
    g = ETGen('/home/user/manifest.xml', '/home/user/manifest_generator.py')
    
if __name__ == '__main__': main()
