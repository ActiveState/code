import os
import select
import subprocess

class MPlayer(object):
    """ A class to access a slave mplayer process
    you may want to use command(name, args*) directly
    or call populate() to access functions (and minimal doc).

    Exemples:
        mp.command('loadfile', '/desktop/funny.mp3')
        mp.command('pause')
        mp.command('quit')

    Note:
        After a .populate() call, you can access an higher level interface:
            mp.loadfile('/desktop/funny.mp3')
            mp.pause()
            mp.quit()

        Beyond syntax, advantages are:
            - completion
            - minimal documentation
            - minimal return type parsing
    """

    exe_name = 'mplayer' if os.sep == '/' else 'mplayer.exe'

    def __init__(self):
        self._mplayer = subprocess.Popen(
                [self.exe_name, '-slave', '-quiet', '-idle'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        self._readlines()

    def _readlines(self):
        ret = []
        while any(select.select([self._mplayer.stdout.fileno()], [], [], 0.6)):
            ret.append( self._mplayer.stdout.readline() )
        return ret

    def command(self, name, *args):
        """ Very basic interface [see populate()]
        Sends command 'name' to process, with given args
        """
        cmd = '%s%s%s\n'%(name,
                ' ' if args else '',
                ' '.join(repr(a) for a in args)
                )
        self._mplayer.stdin.write(cmd)
        if name == 'quit':
            return
        return self._readlines()

    @classmethod
    def populate(kls):
        """ Populates this class by introspecting mplayer executable """
        mplayer = subprocess.Popen([kls.exe_name, '-input', 'cmdlist'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        def args_pprint(txt):
            lc = txt.lower()
            if lc[0] == '[':
                return '%s=None'%lc[1:-1]
            return lc

        while True:
            line = mplayer.stdout.readline()
            if not line:
                break
            if line[0].isupper():
                continue
            args = line.split()
            cmd_name = args.pop(0)
            arguments = ', '.join([args_pprint(a) for a in args])
            func_str = '''def _populated_fn(self, *args):
            """%(doc)s"""
            if not (%(minargc)d <= len(args) <= %(argc)d):
                raise TypeError('%(name)s takes %(argc)d arguments (%%d given)'%%len(args))
            ret = self.command('%(name)s', *args)
            if not ret:
                return None
            if ret[0].startswith('ANS'):
                val = ret[0].split('=', 1)[1].rstrip()
                try:
                    return eval(val)
                except:
                    return val
            return ret'''%dict(
                    doc = '%s(%s)'%(cmd_name, arguments),
                    minargc = len([a for a in args if a[0] != '[']),
                    argc = len(args),
                    name = cmd_name,
                    )
            exec(func_str)

            setattr(MPlayer, cmd_name, _populated_fn)

if __name__ == '__main__':
    import sys
    MPlayer.populate()
    try:
        mp = MPlayer()
        import readline
        readline.parse_and_bind('tab: complete')
        import rlcompleter
        mp.loadfile(sys.argv[1])
        raw_input('Run this with python -i to get interactive shell.'
                '\nPress any key to quit.')
    finally:
        mp.quit()
