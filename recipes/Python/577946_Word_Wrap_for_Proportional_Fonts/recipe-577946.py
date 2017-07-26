import re

def word_wrap(text, width, extent_func):
    '''
    Word wrap function / algorithm for wrapping text using proportional (versus 
    fixed-width) fonts.
    
    `text`: a string of text to wrap
    `width`: the width in pixels to wrap to
    `extent_func`: a function that returns a (w, h) tuple given any string, to
                   specify the size (text extent) of the string when rendered. 
                   the algorithm only uses the width.
    
    Returns a list of strings, one for each line after wrapping.
    '''
    lines = []
    pattern = re.compile(r'(\s+)')
    lookup = dict((c, extent_func(c)[0]) for c in set(text))
    for line in text.splitlines():
        tokens = pattern.split(line)
        tokens.append('')
        widths = [sum(lookup[c] for c in token) for token in tokens]
        start, total = 0, 0
        for index in xrange(0, len(tokens), 2):
            if total + widths[index] > width:
                end = index + 2 if index == start else index
                lines.append(''.join(tokens[start:end]))
                start, total = end, 0
                if end == index + 2:
                    continue
            total += widths[index] + widths[index + 1]
        if start < len(tokens):
            lines.append(''.join(tokens[start:]))
    lines = [line.strip() for line in lines]
    return lines or ['']

if __name__ == '__main__':
    text = (
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua.\n\n'
        'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris '
        'nisi ut aliquip ex ea commodo consequat.\n\n'
        'Duis aute irure dolor in reprehenderit in voluptate velit esse '
        'cillum dolore eu fugiat nulla pariatur.\n\n'
        'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui '
        'officia deserunt mollit anim id est laborum.'
    )
    # dummy extent function behaves like a fixed-width font
    def extent_func(text):
        return (1, 0)
    # wrap to 80 columns
    lines = word_wrap(text, 80, extent_func)
    for line in lines:
        print line
