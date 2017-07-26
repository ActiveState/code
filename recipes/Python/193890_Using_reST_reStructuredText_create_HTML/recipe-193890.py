from docutils import core
from docutils.writers.html4css1 import Writer,HTMLTranslator

class NoHeaderHTMLTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self,document)
        self.head_prefix = ['','','','','']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []

_w = Writer()
_w.translator_class = NoHeaderHTMLTranslator

def reSTify(string):
    return core.publish_string(string,writer=_w)

if __name__ == '__main__':
    test = """
Test example of reST__ document.

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    print reSTify(test)
