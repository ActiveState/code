import sys, argparse

# option decorator
def option(*args, **kwds):
    def _decorator(func):
        _option = (args, kwds)
        if hasattr(func, 'options'):
            func.options.append(_option)
        else:
            func.options = [_option]
        return func
    return _decorator

# arg decorator
arg = option

# combines option decorators
def option_group(*options):
    def _decorator(func):
        for option in options:
            func = option(func)
        return func
    return _decorator


class MetaCommander(type):
    def __new__(cls, classname, bases, classdict):
        subcmds = {}
        for name, func in classdict.items():
            if name.startswith('do_'):
                name = name[3:]
                subcmd = {
                    'name': name,
                    'func': func,
                    'options': []
                }
                if hasattr(func, 'options'):
                    subcmd['options'] = func.options
                subcmds[name] = subcmd
        classdict['_argparse_subcmds'] = subcmds
        return type.__new__(cls, classname, bases, classdict)



class Commander(object):
    __metaclass__ = MetaCommander
    name = 'app'
    description = 'a description'
    version = '0.0'
    epilog = ''
    default_args = []
    
    def cmdline(self):
        parser = argparse.ArgumentParser(
            # prog = self.name,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description=self.__doc__,
            epilog = self.epilog,
        )

        parser.add_argument('-v', '--version', action='version',
                            version = '%(prog)s '+ self.version)

        subparsers = parser.add_subparsers(
            title='subcommands',
            description='valid subcommands',
            help='additional help',
        )
        
        for name in sorted(self._argparse_subcmds.keys()):
            subcmd = self._argparse_subcmds[name]            
            subparser = subparsers.add_parser(subcmd['name'],
                                     help=subcmd['func'].__doc__)
            for args, kwds in subcmd['options']:
                subparser.add_argument(*args, **kwds)
            subparser.set_defaults(func=subcmd['func'])

        if len(sys.argv) <= 1:
            options = parser.parse_args(self.default_args)
        else:
            options = parser.parse_args()
        options.func(self, options)
    


def test():
    # only for options which are repeated across different funcs
    common_options = option_group(
        option('-t', '--type', action='store', help='specify type of package'),
        arg('package', help='package to be (un)installed'),
        option('--log', '-l', action='store_true', help='log is on')
    )
    
    class Application(Commander):
        'a description of the test app'
        name = 'app1'
        version = '0.1'
        default_args = ['install', '--help']
        
        @option('--log', '-l', action='store_true', help='log is on')
        @arg('pattern', help="pattern to delete")
        def do_delete(self, options):
            "help text for delete subcmd"
            print options

        @option('-f', '--force', action='store_true',
                        help='force through installation')
        @common_options
        def do_install(self, options):
            "help text for install subcmd"
            print options

        @common_options
        def do_uninstall(self, options):
            "help text for uninstall subcmd"
            print options

    app = Application()
    app.cmdline()

if __name__ == '__main__':
    test()
