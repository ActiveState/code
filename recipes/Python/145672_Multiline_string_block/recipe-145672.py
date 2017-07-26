import re
...
def formatBlock(block):
        '''Format the given block of text, trimming leading/trailing
        empty lines and any leading whitespace that is common to all lines.
        The purpose is to let us list a code block as a multiline,
        triple-quoted Python string, taking care of indentation concerns.'''
        # separate block into lines
        lines = str(block).split('\n')
        # remove leading/trailing empty lines
        while lines and not lines[0]:  del lines[0]
        while lines and not lines[-1]: del lines[-1]
        # look at first line to see how much indentation to trim
        ws = re.match(r'\s*',lines[0]).group(0)
        if ws:
                lines = map( lambda x: x.replace(ws,'',1), lines )
        # remove leading/trailing blank lines (after leading ws removal)
        # we do this again in case there were pure-whitespace lines
        while lines and not lines[0]:  del lines[0]
        while lines and not lines[-1]: del lines[-1]
        return '\n'.join(lines)+'\n'

# Discussion:
# No one likes to read code that goes
 
            # ...
            htmlFrag = '''
<hr>
<p>Several lines of text
for example's sake.</p>
<hr>
'''
            # do stuff with htmlFrag
            # ...

# This function lets you list them instead as:

            # ...
            htmlFrag = formatBlock('''
                <hr>                            # this block can be
                <p>Several lines of text        # indented to wherever
                for example's sake.</p>         # looks pleasing to you
                <hr>                            #
            ''')
            # do stuff with htmlFrag
            # ...
