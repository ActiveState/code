'''
Generates HTML highlighted code listings for source code files in any language known to 
pygments. For a list of supported formats see http://pygments.org/languages/
by xhuman

'''
import os
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

header = '''<html><head><style>'''
css_close ='''</style><body>'''
footer = '''</body></html>'''

def usage():
    print "\nUsage:", os.path.basename(sys.argv[0]), \
          "[inputFile]", "[outputFile]", "[lexer]"

def getHtml(fileName=None, lexer_name='python', user_css_class="code"):

    if not lexerName:
        lexer = get_lexer_for_filename(os.path.basename(fileName))
    else:

        try:
            lexer = get_lexer_by_name(lexer_name)
        except IndexError:
            print 'Error: no such lexer:',lexer_name
            usage()
            sys.exit(-2)

    formatter = HtmlFormatter(linenos=True, cssclass=user_css_class)
    code = open(fileName).read()
    return highlight(code, lexer, formatter)

if __name__ == '__main__':
    in_file = None
    out_file = None
    css_class_name = 'code'
    css = HtmlFormatter().get_style_defs('.' + css_class_name)

    if len(sys.argv) >1:
        in_file = sys.argv[1]
    else:
        usage()
        sys.exit(-1)

    if len(sys.argv) >2:
        out_file = sys.argv[2]
    else:
        out_file = os.sys.stdout

    if len(sys.argv) > 3:
        lexerName = sys.argv[3]
    else:
        lexerName = None
    
    result = getHtml(in_file,lexerName,css_class_name)

    output ="\n".join([header,css,css_close, result,footer])

    if out_file != os.sys.stdout:
        open(out_file,"w").write(output)
    else:
        print output
