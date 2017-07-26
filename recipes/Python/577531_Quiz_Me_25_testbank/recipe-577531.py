####################
# source/testbank.py
####################

from xml.sax import parse as _parse
from xml.sax.handler import ContentHandler as _ContentHandler

################################################################################

class BankParser(_ContentHandler):

    def __init__(self):
        super().__init__()
        self.context = []

    def startElement(self, name, attrs):
        if name == 'testbank':
            # Validate
            assert len(self.context) == 0
            # Specific
            name = attrs.getValue('name')
            self.context.append(TestBank(name))
        elif name == 'chapter':
            # Validate
            assert isinstance(self.context[-1], TestBank)
            # Specific
            name = attrs.getValue('name')
            self.context.append(Chapter(name))
        elif name == 'section':
            # Validate
            assert isinstance(self.context[-1], Chapter)
            # Specific
            name = attrs.getValue('name')
            self.context.append(Section(name))
        elif name == 'category':
            # Validate
            assert isinstance(self.context[-1], Section)
            # Specific
            kind = attrs.getValue('type')
            assert kind in ('multiple_choice', 'true_or_false', 'matching')
            self.context.append(Category(kind))
        elif name == 'fact':
            # Validate
            assert isinstance(self.context[-1], Category)
            # Specific
            if self.context[-1].attr == 'multiple_choice':
                kind = attrs.getValue('type')
                self.context.append(Fact(kind))
            else:
                self.context.append(Fact())
        elif name == 'question':
            # Validate
            assert isinstance(self.context[-1], Fact)
            # Specific
            self.context.append(Question())
        elif name == 'answer':
            # Validate
            assert isinstance(self.context[-1], Fact)
            # Specific
            self.context.append(Answer())
        else:
            # Something is wrong with this document.
            raise ValueError(name)

    def characters(self, content):
        self.context[-1].add_text(content)

    def endElement(self, name):
        node = self.context.pop()
        if name == 'testbank':
            self.TESTBANK = node
        else:
            self.context[-1].add_child(node)

################################################################################

class _Node:

    def __init__(self, attr=None):
        self.attr = attr
        self.text = ''
        self.children = []

    def __repr__(self):
        name = self.__class__.__name__.lower()
        if self.attr is None:
            attr = ''
        else:
            attr = ' {}="{}"'.format(self.ATTR_NAME, self.attr)
        cache = '<{}{}>'.format(name, attr)
        for child in self.children:
            lines = repr(child).split('\n')
            lines = map(lambda line: '    ' + line, lines)
            cache += '\n' + '\n'.join(lines)
        cache += self.text if self.ATTR_NAME is None else '\n'
        cache += '</{}>'.format(name)
        return cache

    def add_text(self, content):
        self.text += content

    def add_child(self, node):
        self.children.append(node)

################################################################################

class TestBank(_Node): ATTR_NAME = 'name'
class Chapter(_Node): ATTR_NAME = 'name'
class Section(_Node): ATTR_NAME = 'name'
class Category(_Node): ATTR_NAME = 'type'
class Fact(_Node): ATTR_NAME = 'type'
class Question(_Node): ATTR_NAME = None
class Answer(_Node): ATTR_NAME = None

################################################################################

def parse(filename):
    parser = BankParser()
    _parse(filename, parser)
    return parser.TESTBANK
