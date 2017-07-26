#    Trivia
#    Copyright (C) 2005  Petko Petkov (GNUCITIZEN) ppetkov@gnucitizen.org
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import re

class Template(unicode):
    """
    Trivia Template Object
    """

    def __init__(self, string):
        self.code = None
        unicode.__init__(self, string)
        self.compile()

    def __mod__(self, globals):
        """
        x.__mod__(globals) <==> x % other

        Expand template using globals.
        """

        locals = {'_':''}

        exec self.code in globals, locals

        return locals['_']

    def tokenize(self):
        """
        tokenize(self) -> generator

        Split self into tokens and return generator object.
        """
        for token in re.split('(<\?.*?\?>)', self):
            if token.startswith('<?') and token.endswith('?>'):
                yield token

            else:
                for ref in re.split('(###[\w_.]*)', token):
                    yield ref

    def compile(self):
        """
        compile(self) -> None

        Compile self into Python code.
        """

        if self.code is not None:
            return

        level = 0
        source = ''

        for token in self.tokenize():
            indent = ' ' * level * 2

            if token.startswith('###'):
                source = source + '%s_ = _ + %s\n' % \
                    (indent, token[3:].strip())

            elif token.startswith('<?') and token.endswith('?>'):
                content = token[2:-2]

                if content == 'end':
                    level = level - 1

                elif content.startswith('if ') \
                or content.startswith('for ') \
                or content.startswith('while '):
                    source = source + '%s%s:\n' % (indent, content)
                    level = level + 1

                elif content.startswith('='):
                    source = source + '%s_ = _ + %s\n' % \
                        (indent, content[1:].strip())

            else:
                source = source + '%s_ = _ + """%s"""\n' % \
                    (indent, token.replace('"""', r'\"\"\"'))

        self.code = compile(source, '<string>', 'exec')
