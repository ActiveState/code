shell.py:
import sys

class Shell:
    def __init__(self):
        self.prefix = '/bin'
        self.env = {}
        self.stdout = None
        self.stderr = None
        self.wait = False

    def __getattr__(self, command):
        def __call(*args, **keywords):
            if command == 'prefix':
                return self.prefix
            if command == 'stdout':
                return self.stdout
            if command == 'stderr':
                return self.stderr
            if command.startswith('__'):
                return None
            if self.prefix:
                exe = '%s/%s' % (self.prefix, command)
            else:
                exe = command
            import os, subprocess
            if os.path.exists(exe):
                exeargs = [exe]
                if keywords:
                    for i in args.iteritems(): exeargs.extend(i)
                if args:
                    exeargs.extend(args)
                exeargs = [str(i) for i in exeargs]
                cwd = os.path.abspath(os.curdir)
                p = subprocess.Popen(exeargs, bufsize=1, cwd=cwd, env=self.env, stdout=subprocess.PIPE, close_fds=False, universal_newlines=True)
                if self.wait:
                    ret = p.wait()
                else:
                    ret = p.returncode
                result = None
                if p.stdout:
                    self.stdout = p.stdout.readlines()
                if p.stderr:
                    self.stderr = p.stderr.readlines()
                return ret
            else:
                raise Exception('No executable found at %s' % exe)
        return __call

sys.modules[__name__] = Shell()
