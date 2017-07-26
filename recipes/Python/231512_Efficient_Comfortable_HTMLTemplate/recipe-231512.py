#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
This module is the B{Template Macro} module. It preprocesses a web 
template in which variables and blocks are contained. This package 
plays an important role as an explicit boundary between web template 
designing and script implementation.

@note: A block can be defined with block comment:
C{<!-- block }M{q}C{ start -->}
M{c}
C{<!-- block }M{q}C{ end -->},
where M{q} is the block name and M{c} is the content of this block.

@note: It should be noted that each subblock symbol is necessary to 
differ from its superblock's name. This is owing to the block pattern.

@author: Prachya Boonkwan
@organization: NAI{i}ST Laboratory, Kasetsart University, Thailand
@copyright: October 23, 2003
'''

########################################

import copy
import re
import string

########################################

class Template:
    '''
    Web template representation. As soon as the template instance is 
    constructed, the content is automatically analyzed and the symbol 
    table is afterward created.

    @ivar path: Path to web template file.
    @type path: str
    @ivar content: Textual content of web template.
    @type content: str
    @ivar symtab: Symbol table of web template
    @type symtab: dict

    @cvar blkpat: Block declaration pattern (regular expression). It
    should be noted that this pattern does I{not} greedily match the
    block body.
    '''

    blkpat = re.compile(
        r'\s*<!---*\s*block\s*(?P<blkname>\w+?)\s*(start|begin)\s*-*-->'
        r'(?P<blkbody>\s*.*?)'
        r'\s*<!---*\s*block\s*(?P=blkname)\s*end\s*-*-->',
        re.DOTALL
    )

    def __init__(self, path = None, content = None, symtab = None):
        '''
        Construct a web template representation.

        @param path: Path to web template file.
        @type path: str
        @param content: Textual content of web template
        @type content: str
        @param symtab: Symbol table of web template
        @type symtab: dict
        
        @note: It is recommended to specify only the path of the 
        template.
        '''

        if symtab is None: symtab = {}

        self.path = path
        self.content = content
        self.symtab = symtab

        if self.content is None or len(self.symtab) == 0:
            if self.path is not None:
                self.load()
            self.content = self.analyze(self.content)

    def __copy__(self):
        '''
        Copy a web template representation.
        '''

        return Template(
            self.path, self.content, copy.copy(self.symtab)
        )

    def load(self):
        '''
        Load the content of the template from the specified path.
        '''

        fhdl = open(self.path)
        self.content = fhdl.read()
        fhdl.close()

    def analyze(self, text, blkpath = None):
        '''
        Analyze the text to establish blocks.

        @param text: Text to be analyzed.
        @type text: str
        @param blkpath: Block path to the text.
        @type blkpath: list

        @return: Content which blocks are replaced with symbols.
        @rtype: str

        @raise TemplateError: If symbol reassignment occurs.
        '''

        if blkpath is None: blkpath = []

        result = text

        while True:
            matobj = Template.blkpat.search(result)
            if matobj is None: break
            blkname = matobj.group('blkname')
            symbol = string.join(blkpath + [blkname], '.')
            blkbody = matobj.group('blkbody')
            (result, _) = Template.blkpat.subn(
                '[[:%s:]]' % symbol, result, 1
            )
            value = self.analyze(blkbody, blkpath + [blkname])

            if symbol not in self.symtab.keys():
                self.symtab[symbol] = value
            else:
                raise TemplateError, \
                'Reassigning the same symbol (%s).' % symbol

        return result

    def __getitem__(self, symbol):
        '''
        Get the value of the symbol.

        @param symbol: Symbol name.
        @type symbol: str

        @return: Value of the symbol.
        @rtype: str
        '''

        return self.symtab[symbol]

    def repr(self):
        '''
        Represent this template with a string representation.

        @return: String C{Template(path = }M{p}C{, content = }M{c}
        C{, symtab = }M{s}C{)}, where M{p} is the path, M{c} is the 
        content of that template, and M{s} is the symbol table.
        @rtype: str
        '''

        return 'Template(path = %r, content = %r, symtab = %r)' % (
            self.path, self.content, self.symtab
        )

    __repr__ = __str__ = repr

########################################

class TemplateError(Exception):
    '''
    Error occurring in the class Template.
    '''

    pass

########################################

class PageMacro:
    '''
    Page Macro Expander. It enables users to define symbols in order 
    to be expanded to templates further. Moreover, also enables users 
    to expand consecutively blocks in templates.

    @ivar symtab: Symbol table.
    @type symtab: dict

    @cvar KEEPMODE: Mode of keeping all undefined symbols.
    @type KEEPMODE: int
    @cvar DELMODE: Mode of deleting all undefined symbols.
    @type DELMODE: int

    @cvar varpat: Symbol pattern.
    @cvar unkpat: Unknown symbol pattern.
    '''

    KEEPMODE = 0
    DELMODE = 1

    varpat = re.compile(r'\[\[:(?P<symname>(\w+\.)*\w+?):\]\]')
    unkpat = re.compile(r'\[\[::(?P<synname>(\w+\.)*\w+?)::\]\]')

    def __init__(self, mainsym, unkmthd = None, symtab = None):
        '''
        Construct a page macro expander.

        @param mainsym: Main symbol to be displayed.
        @type mainsym: str
        @param unkmthd: Resolution method of undefined symbols
        (C{PageMacro.KEEPMODE} or C{PageMacro.DELMODE}).
        @type unkmthd: int
        @param symtab: Symbol table.
        @type symtab: dict
        '''

        if unkmthd is None: unkmthd = PageMacro.KEEPMODE
        if symtab is None: symtab = {}

        self.mainsym = mainsym
        self.unkmthd = unkmthd
        self.symtab = symtab

    def __copy__(self):
        '''
        Copy a page macro expander.
        '''

        return PageMacro(
            self.mainsym, self.unkmthd, copy.copy(self.symtab)
        )

    def repr(self):
        '''
        Represent a page macro expander with a string representation.

        @return: String C{PageMacro(mainsym = }M{q}C{, unkmthd = }M{m}
        C{, symtab = }M{s}C{)}, where M{q} is the main symbol, M{m} is 
        the resolution method of unknown or undefined symbols and M{s} 
        is the symbol table.
        @rtype: str
        '''

        return 'PageMacro(mainsym = %s, unkmthd = %d, symtab = %r)' % (
            self.mainsym, self.unkmthd, self.symtab
        )

    __repr__ = repr

    def __getitem__(self, symbol):
        '''
        Get the value of a symbol.

        @param symbol: Symbol name.
        @type symbol: str

        @return: Value of the symbol.
        @rtype: Template
        '''

        return self.symtab[symbol]

    def __setitem__(self, symbol, value):
        '''
        Set the value of a symbol.

        @param symbol: Symbol name.
        @type symbol: str
        @param value: Value of the symbol.
        @type value: str or Template

        @note: The parameter C{value} of a symbol can be a string or a
        template. If it is a string, it will be considered as the
        content of the template and it will be wrapped with Template
        class. On the contrary, if it is a template, it will be
        directly assigned to the symbol.

        @note: If users would like to assign to a symbol with the path
        to a template file, please use C{pm[}M{s}C{] = 
        Template(path = }M{p}C{)}, where C{pm} is a C{PageMacro} 
        instance, M{s} is a symbol name, and M{p} is a path to 
        template. Users can alternatively use the method C{load} for
        ease of use.

        @note: If users would like to assign directly to a symbol with
        the template content, please use C{pm[}M{s}C{] = }M{c}, where 
        C{pm} is a C{PageMacro} instance and M{c} is a content of
        template.
        '''

        if isinstance(value, Template):
            self.symtab[symbol] = value
        elif type(value) is str:
            self.symtab[symbol] = Template(content = value)

    def load(self, symbol, filename):
        '''
        Load a template file to a symbol.

        @param symbol: Symbol name.
        @type symbol: str
        @param filename: Template path.
        @type filename: str
        '''

        self[symbol] = Template(path = filename)

    def resolve(self, symbol):
        '''
        Resolve the specified symbol to absolute value.

        @param symbol: Symbol name.
        @type symbol: str

        @return: Absolute value of the symbol.
        @rtype: str
        '''

        if symbol not in self.symtab:
            return '[[::%s::]]' % symbol

        result = self.symtab[symbol].content

        while True:
            matobj = PageMacro.varpat.search(result)
            if matobj is None: break
            symname = matobj.group('symname')
            if symname in self.symtab:
                (result, _) = PageMacro.varpat.subn(
                    self.resolve(symname), result, 1
                )
            else:
                (result, _) = PageMacro.varpat.subn(
                    '[[::%s::]]' % symname, result, 1
                )

        return self.handle_unk(result)

    def handle_unk(self, text):
        '''
        Handle unknown symbols in the text.

        @param text: Text.
        @type text: str

        @return: Unknown-handled text.
        @rtype: str
        '''

        result = text

        while True:
            matobj = PageMacro.unkpat.search(result)
            if matobj is None: break
            if self.unkmthd == PageMacro.KEEPMODE:
                result = PageMacro.unkpat.sub(
                    '[[:\g<synname>:]]', result
                )
            elif self.unkmthd == PageMacro.DELMODE:
                result = PageMacro.unkpat.sub('', result)

        return result

    def envision(self, tempsym, blocksym, symdict):
        '''
        Resolve a block in a template with a symbol dictionary.

        @param tempsym: Template symbol.
        @type tempsym: str
        @param blocksym: Block symbol in the template.
        @type blocksym: str
        @param symdict: Symbol dictionary.
        @type symdict: dict

        @raise PageMacroError: If unknown switch is to be resolved.
        '''

        self.expand(tempsym, blocksym, [symdict])

    def expand(self, tempsym, blocksym, iterable):
        '''
        Expand consecutively a block in a template with an iterable.

        @param tempsym: Template symbol.
        @type tempsym: str
        @param blocksym: Block symbol in the template.
        @type blocksym: str
        @param iterable: Iterable list of dictionaries whose keys and
        values resemble correspondences among symbols and their 
        values. A value in the dictionary can be a list or an iterable
        to expand recursively the block. In this case, the key of such
        value is necessary to specify explicitly block hierarchy.
        @type iterable: list or iter

        @raise PageMacroError: If unknown block is to be resolved.
        '''

        if (
            tempsym not in self.symtab
        ):
            raise PageMacroError, \
            'Unknown template (%s) cannot be resolved.' % tempsym
            
        if (
            blocksym not in self.symtab[tempsym].symtab
        ):
            raise PageMacroError, \
            'Unknown block (%s) cannot be resolved.' % blocksym

        result = []

        for symdict in iterable:
            content = self.symtab[tempsym][blocksym]

            while True:
                matobj = PageMacro.varpat.search(content)
                if matobj is None: break
                symname = matobj.group('symname')
                
                if symname in symdict:
                    if type(symdict[symname]) is str:
                        self[symname] = symdict[symname]
                    elif type(symdict[symname]) in [list, iter]:
                        self.expand(tempsym, symname, symdict[symname])
                    elif type(symdict[symname]) is dict:
                        self.expand(
                            tempsym, symname, [symdict[symname]]
                        )

                (content, _) = PageMacro.varpat.subn(
                    self.resolve(symname), content, 1
                )

            result.append(content)

        self[blocksym] = string.join(result, '')

    def str(self):
        '''
        Represent a page macro expander with the expanded value of the 
        main symbol.

        @return: Expanded value.
        @rtype: str
        '''

        return self.resolve(self.mainsym)

    __str__ = str

########################################

class PageMacroError(Exception):
    '''
    Error occurring in the class PageMacro.
    '''

    pass

########################################

def demo():
    '''
    Demonstrate this module.
    '''
    
    input = '''
<html>
    This page was written by <b>[[:author:]]</b>.
    <!-- block TableBlock start -->
    <table>
        <th>
            <td>[[:h1:]]</td>
            <td>[[:h2:]]</td>
            <td>[[:h3:]]</td>
        </th>
        <!-- block RowBlock start -->
        <tr>
            <td>[[:c1:]]</td>
            <td>[[:c2:]]</td>
            <td>[[:c3:]]</td>
        </tr>
        <!-- block RowBlock end -->
    </table>
    <!-- block TableBlock end -->
</html>
    '''

    pm = PageMacro('Content', PageMacro.DELMODE)
    pm['Content'] = input
    pm['author'] = 'Prachya Boonkwan'
    pm.expand('Content', 'TableBlock', [
        {
            'h1': 'Country', 'h2': 'President', 'h3': 'Population',
            'TableBlock.RowBlock': [
                {'c1': 'USA', 'c2': 'Bush', 'c3': '200m'},
                {'c1': 'PRC', 'c2': 'Jintao', 'c3': '1,200m'}
            ]
        },
        {
            'h1': 'Class', 'h2': 'Instructor', 'h3': 'Student No.',
            'TableBlock.RowBlock': [
                {'c1': 'AI', 'c2': 'AK', 'c3': '60'},
                {'c1': 'NLP', 'c2': 'AK', 'c3': '50'}
            ]
        }
    ])
    print pm

if __name__ == '__main__':
    demo()
