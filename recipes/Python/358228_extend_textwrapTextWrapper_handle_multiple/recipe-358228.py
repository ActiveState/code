"""Wrap textwrap.TextWrapper to properly handle multiple paragraphs"""

import textwrap
import re

class DocWrapper(textwrap.TextWrapper):
    """Wrap text in a document, processing each paragraph individually"""

    def wrap(self, text):
        """Override textwrap.TextWrapper to process 'text' properly when
        multiple paragraphs present"""
        para_edge = re.compile(r"(\n\s*\n)", re.MULTILINE)
        paragraphs = para_edge.split(text)
        wrapped_lines = []
        for para in paragraphs:
            if para.isspace():
                if not self.replace_whitespace:
                    # Do not take the leading and trailing newlines since
                    # joining the list with newlines (as self.fill will do)
                    # will put them back in.
                    if self.expand_tabs:
                        para = para.expandtabs()
                    wrapped_lines.append(para[1:-1])
                else:
                    # self.fill will end up putting in the needed newline to
                    # space out the paragraphs
                    wrapped_lines.append('')
            else:
                wrapped_lines.extend(textwrap.TextWrapper.wrap(self, para))
        return wrapped_lines



if __name__ == '__main__':
    import optparse
    import sys

    default_wrapper = DocWrapper()

    parser = optparse.OptionParser()
    parser.add_option('-w', '--width', dest="width",
            default=default_wrapper.width, type='int',
            help="maximum length of wrapped lines")
    parser.add_option('-t', '--tabs', dest="expand_tabs",
            default=False, action="store_true",
            help="Expand tabs")
    parser.add_option('-s', '--whitespace', dest='replace_whitespace',
            default=False, action="store_true",
            help="Replace whitespace")

    options, args = parser.parse_args()

    if len(args) > 1:
        print "You may only specify a single file"
        sys.exit(1)

    if not args:
        text = sys.stdin.read()
    else:
        try:
            FILE = open(args[0], 'rU')
            text = FILE.read()
        finally:
            FILE.close()
    wrapper = DocWrapper(width=options.width, expand_tabs=options.expand_tabs,
            replace_whitespace=options.replace_whitespace)
    print wrapper.fill(text)
