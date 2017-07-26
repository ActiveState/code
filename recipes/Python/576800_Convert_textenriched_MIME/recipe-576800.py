"""
Convert text/enriched MIME type to text/html MIME type.

Based on the program in Appendix B of RFC 1896 -- see
http://www.rfc-editor.org/rfc/rfc1896.txt. 

However, it was entirely rewritten for Python and 
refactored for flexibility and comprehension. Support 
for color and fontfamily was added.

Usage: python enriched2html.py < source.txt > target.html
"""
__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="May 2009"

import array
import sys
import os, os.path


class StdIo(array.array):
    """ Wraps array to provide C stdio functions 
    for a block of text. """
    def __new__(cls, tc='c'):
        return super(StdIo, cls).__new__(cls, 'c')
    
    def __init__(self, s=""):
        self.fromstring(s)
        self.position = 0

    def __repr__(self):
        return self.tostring()
        
    def getc(self):
        if self.position < len(self):
            c = self[self.position]
            self.position += 1
        else:
            c = None
        return c
    
    def lookaheadc(self):
        c = self.getc()
        self.ungetc(c)
        return c
    
    def ungetc(self, c):
        if c != None:
            if self.position > 0:
                self.position -= 1

    def putc(self, c):
        self.append(c)

    def puts(self, s):
        self.fromstring(s)

    def get_text_until(self, delimiters=()):
        chars = []
        c = self.getc()
        while c and c not in delimiters:
            chars.append(c)
            c = self.getc()
        text = "".join(chars)
        return c, text
        
        
COMMAND_MAP = {
    "param": "",
    "nofill": "pre",
    "bold": "b",
    "italic": "i",
    "underline": "u",
    "fixed": "tt",
    "center": "center",
    "excerpt": "blockquote",
    "color": "font",
    "fontfamily": "font",
#____UNIMPLEMENTED____
    "paraindent": "",
    "indentright": "",
    "flushleft": "",
    "flushright": "",
    "flushboth": "",
    "bigger": "",
    "smaller": "",
    "indent": ""
}

class TextBlock(object):
    """ Wraps a block of text """
    def __init__(self):
        self.text = ""
        
    def __repr__(self):
        return "[%s]" % self.text
        
class CommandBlock(TextBlock):
    """ TextBlock in which the text is the command plus end flag
    param list """
    def __init__(self):
        TextBlock.__init__(self)
        self.end = False
        self.params = []

    def __repr__(self):
        return "[cmd: %s end: %d]" % (self.text, self.end)

                
def is_text_block(block):
    return (block and isinstance(block, TextBlock))

def is_command_block(block):
    return (block and isinstance(block, CommandBlock))

def is_param_block(block):
    return (is_command_block(block) and block.text == "param")

def is_end_param_block(block):
    return (is_param_block(block) and block.end == True)


class Converter(object):
    """ Converts text/enriched text to text/html format by first
    splitting into a stream of text blocks and command blocks,
    then processing those  blocks into html code. """
    def __init__(self, text):
        self.text = text
        self.input = None
        self.output = None
        self.blocks  = []
        self.block_index = 0
        self.no_fill_count = 0
        
    def execute(self):
        text = self.convert(self.text)
        return text
    
    def convert(self, text):        
        self.input = StdIo(text)
        self.output = StdIo()
        self.read_blocks()
        #self.debug_blocks()
        self.write_blocks()
        self.output.puts('\n')   
        return str(self.output)
    
    def get_block(self):
        if self.block_index < len(self.blocks):
            block = self.blocks[self.block_index]
            self.block_index += 1
        else:
            block = None
        return block

    def unget_block(self, block):
        if block:
            if self.block_index > 0:
                self.block_index -= 1
            
    def get_params(self, command_block):
        while True:
            block_1 = self.get_block()
            block_2 = self.get_block()
            block_3 = self.get_block()
            if is_param_block(block_1) and is_text_block(block_2) and is_end_param_block(block_3):
                command_block.params.append(block_2.text)
            else:
                self.unget_block(block_3)
                self.unget_block(block_2)
                self.unget_block(block_1)
                break
            
    def write_blocks(self):
        self.block_index = 0
        block = self.get_block()
        while block:
            if is_command_block(block) and not block.end:
                self.get_params(block)
            if is_command_block(block):
                self.write_command_block(block)
            elif is_text_block(block):
                self.write_text_block(block)
            block = self.get_block()   
    
    def write_command_block(self, block):
        command = block.text
        html_command = ""
        mapped_command = COMMAND_MAP.get(command, "")
        if not mapped_command:
            if not block.end:
                mapped_command = "?" + command
            else:
                mapped_command = "?" + command
                
        if not block.end:
            if command == "color":
                html_command =("<%s color=\"%s\">" % (mapped_command, block.params[0]))
            elif command == "fontfamily":
                html_command =("<%s face=\"%s\">" % (mapped_command, block.params[0]))
            else:
                html_command = ("<%s>" % mapped_command)
        else:
            html_command = ("</%s>" % mapped_command)
        
        if command == "nofill":
            if not block.end:
                self.no_fill_count += 1
            else:
                self.no_fill_count -= 1
            
        self.output.puts(html_command)

    def write_text_block(self, block):
        newline_count = 0
        for c in block.text:
            if c == '\n' and self.no_fill_count <= 0:
                if newline_count == 0:
                    c = ' '
                newline_count += 1
            else:
                newline_count = 0
                
            if c == '<':
                c = "&lt;"
            elif c == '>':
                c = "&gt;"
            elif c == '&':
                c = "&amp;"
            elif c == '\n':
                if self.no_fill_count <= 0:
                    c = "<br/>"
            self.output.puts(c)

    def debug_blocks(self):
        block = self.get_block()
        while block:
            print block
            block = self.get_block()

    def read_command_block(self, c):
        block = CommandBlock()
        c, text = self.input.get_text_until(">")
        if text and text[0] == '/':
            text = text[1:]
            block.end = True
        block.text = text.lower()
        return c, block
        
    def read_text_block(self, c):
        block = TextBlock()
        c2, text = self.input.get_text_until('<')
        block.text = c + text   
        if c2 == '<':
            self.input.ungetc(c2)
        return c2, block
        
    def read_blocks(self):
        c = self.input.getc()
        while c:
            if c == '<':
                if self.input.lookaheadc() == '<':
                    c = self.input.getc()
                    c, block = self.read_text_block('<')
                else:
                    c, block = self.read_command_block('<')
            else:
                c, block = self.read_text_block(c)
            self.blocks.append(block)
            c = self.input.getc()      

def convert_file(fp_in=sys.stdin):
    text = fp_in.read()
    html = Converter(text).execute()
    return html

def output_html(html, fp_out=sys.stdout):
    fp_out.write(html)

def main():
    html = convert_file()
    output_html(html)
    
if __name__ == "__main__":
    main()
