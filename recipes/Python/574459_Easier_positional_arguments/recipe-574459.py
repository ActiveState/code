import sys
from optparse import OptionParser, Option, SUPPRESS_HELP

class PAOptionParser(OptionParser, object):
    def __init__(self, *args, **kw):
        self.posargs = []
        super(PAOptionParser, self).__init__(*args, **kw)

    def add_posarg(self, *args, **kw):
        pa_help = kw.get("help", "")
        kw["help"] = SUPPRESS_HELP
        o = self.add_option("--%s" % args[0], *args[1:], **kw)
        self.posargs.append((args[0], pa_help))

    def get_usage(self, *args, **kwargs):
        self.usage = "%%prog %s [options]\n\nPositional Arguments:\n %s" % \
        (' '.join(["<%s>" % arg[0] for arg in self.posargs]), '\n '.join(["%s: %s" % (arg) for arg in self.posargs]))
        return super(self.__class__, self).get_usage(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        args = sys.argv[1:]
        args0 = []
        for p, v in zip(self.posargs, args):
            args0.append("--%s" % p[0])
            args0.append(v)
        args = args0 + args
        options, args = super(self.__class__, self).parse_args(args, **kwargs)
        if len(args) < len(self.posargs):
            msg = 'Missing value(s) for "%s"\n' % ", ".join([arg[0] for arg in self.posargs][len(args):])
            self.error(msg)
        return options, args

if __name__ == '__main__':
    #parser = PAOptionParser("My usage str")
    parser = PAOptionParser()
    parser.add_posarg("Foo", help="Foo usage")
    parser.add_posarg("Bar", dest="bar_dest")
    parser.add_posarg("Language", dest='tr_type', type="choice", choices=("Python", "Other"))
    parser.add_option('--stocksym', dest='symbol')
    values, args = parser.parse_args()
    print values, args

# python mycp.py  -h
# python mycp.py
# python mycp.py  foo
# python mycp.py  foo bar
#
# python mycp.py foo bar lava
# Usage: pa.py <Foo> <Bar> <Language> [options]

# Positional Arguments:
# Foo: Foo usage
# Bar: 
# Language: 
#
# pa.py: error: option --Language: invalid choice: 'lava' (choose from 'Python', 'Other')
