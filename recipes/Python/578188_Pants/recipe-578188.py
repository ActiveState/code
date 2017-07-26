# THIS IS A PORT OF ANOTHER PROGRAM

import sys, os

p, a = (sys.argv + [None])[:2]

def echo(string, newline=False):
    sys.stdout.write(string + (newline and '\n' or ''))

def start():
    echo("Putting on pants ...", True)
    if os.stat(p).st_mode == 33206:
        echo("one leg at a time.")
        os.chmod(p, 256)
    else:
        echo("Looks like we've still got some old pants on. They'll do.")

def stop(newline=False):
    echo("Taking off pants ...", newline)
    os.chmod(p, 128)

def restart():
    echo("Time for a change of pants.", True)
    stop(True)
    start()

def status():
    if os.stat(p).st_mode == 33060:
        echo("Pants are on.")
    else:
        echo("We're not wearing any pants.")

if a in ('start', 'stop', 'restart', 'status'):
    globals()[a]()
else:
    echo("Usage: %s {start|stop|restart|status}" % os.path.basename(p))
