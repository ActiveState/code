'''shellcmd - simple invocation of shell commands from Python'''

def shell_call(cmd, *args, **kwds):
    if args or kwds:
        cmd = cmd.format(*args, **kwds)
    return subprocess.call(cmd, shell=True)

def check_shell_call(cmd, *args, **kwds):
    if args or kwds:
        cmd = cmd.format(*args, **kwds)
    return subprocess.check_call(cmd, shell=True)

def check_shell_output(cmd, *args, **kwds):
    if args or kwds:
        cmd = cmd.format(*args, **kwds)
    return subprocess.check_output(cmd, shell=True)
