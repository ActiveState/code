import re

LEFT = '<'
RIGHT = '>'
CENTER = '^'

class FormatColumns:
    '''Format some columns of text with constraints on the widths of the
    columns and the alignment of the text inside the columns.
    '''
    def __init__(self, columns, contents, spacer=' | ', retain_newlines=True):
        '''
        "columns"   is a list of tuples (width in chars, alignment) where
                    alignment is one of LEFT, CENTER or RIGHT.
        "contents"  is a list of chunks of text to format into each of the
                    columns.
        '''
        assert len(columns) == len(contents), \
            'columns and contents must be same length'
        self.columns = columns
        self.num_columns = len(columns)
        self.contents = contents
        self.spacer = spacer
        self.retain_newlines = retain_newlines
        self.positions = [0]*self.num_columns

    def format_line(self, wsre=re.compile(r'\s+')):
        ''' Fill up a single row with data from the contents.
        '''
        l = []
        data = False
        for i, (width, alignment) in enumerate(self.columns):
            content = self.contents[i]
            col = ''
            while self.positions[i] < len(content):
                word = content[self.positions[i]]
                # if we hit a newline, honor it
                if '\n' in word:
                    # chomp
                    self.positions[i] += 1
                    if self.retain_newlines:
                        break
                    word = word.strip()

                # make sure this word fits
                if col and len(word) + len(col) > width:
                    break

                # no whitespace at start-of-line
                if wsre.match(word) and not col:
                    # chomp
                    self.positions[i] += 1
                    continue

                col += word
                # chomp
                self.positions[i] += 1
            if col:
                data = True
            if alignment == CENTER:
                col = '{:^{}}'.format(col.strip(), width)
            elif alignment == RIGHT:
                col = '{:>{}}'.format(col.rstrip(), width)
            else:
                col = '{:<{}}'.format(col.lstrip(), width)
            l.append(col)

        if data:
            return self.spacer.join(l).rstrip()
        # don't return a blank line
        return ''

    def format(self, splitre=re.compile(r'(\n|\r\n|\r|[ \t]|\S+)')):
        # split the text into words, spaces/tabs and newlines
        for i, content in enumerate(self.contents):
            self.contents[i] = splitre.findall(content)

        # now process line by line
        l = []
        line = self.format_line()
        while line:
            l.append(line)
            line = self.format_line()
        return '\n'.join(l)

    def __str__(self):
        return self.format()

def wrap(text, width=75, alignment=LEFT):
    return FormatColumns(((width, alignment),), [text])
