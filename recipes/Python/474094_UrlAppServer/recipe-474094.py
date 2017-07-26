from urllib import unquote_plus
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from traceback import format_exc
import sys

def parse(url):
    return [unquote_plus(x) for x in url.split("/") if x!='']

def locate(root, args):
    curr = root
    i = 0;
    for a in args:
        try:
            curr = getattr(curr, a)
        except AttributeError:
            return curr, args[i:]
        i += 1
    return curr, []

def run(fun, args, input, output):
    sys.stdin  = input
    sys.stdout = output
    fun(args)
    sys.stdin  = sys.__stdin__
    sys.stdout = sys.__stdout__

class UrlAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = parse(self.path)
        fun,args = locate(self.server, args)
        self.send_response(200)
        self.end_headers()
        try:
            run(fun, args, self.rfile, self.wfile)
        except:
            self.wfile.write(format_exc())

class UrlApp:
    def __call__(self, *a, **kw): pass

class UrlAppServer(HTTPServer, UrlApp):
    def __init__(self, addr):
        HTTPServer.__init__(self, addr, UrlAppHandler)

#### EXAMPLE ##########################################################

def echo(args):
    for a in args:
        print a

from operator import add
def sum(args):
    print reduce(add, map(int, args))

root = UrlAppServer(('0.0.0.0',1234))
root.apps = UrlApp() # provide 'apps' folder for our functions
root.apps.echo = echo
root.apps.sum = sum

root.serve_forever()

# now point Your web browser to:
#   http://127.0.0.1:1234/apps/echo/None shall pass!
#   http://127.0.0.1:1234/apps/sum/1/2/4/8/16/8/3
#   http://127.0.0.1:1234/apps/sum/1/2/3/five
