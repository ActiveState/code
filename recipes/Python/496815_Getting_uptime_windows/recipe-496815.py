def uptime():
    """Returns a datetime.timedelta instance representing the uptime in a Windows 2000/NT/XP machine"""
    import os, sys
    import subprocess
    if not sys.platform.startswith('win'):
        raise RuntimeError, "This function is to be used in windows only"
    cmd = "net statistics server"
    p = subprocess.Popen(cmd, shell=True, 
          stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    (child_stdin, child_stdout) = (p.stdin, p.stdout)
    lines = child_stdout.readlines()
    child_stdin.close()
    child_stdout.close()
    lines = [line.strip() for line in lines if line.strip()]
    date, time, ampm = lines[1].split()[2:5]
    #print date, time, ampm
    m, d, y = [int(v) for v in date.split('/')]
    H, M = [int(v) for v in time.split(':')]
    if ampm.lower() == 'pm':
        H += 12
    import datetime
    now = datetime.datetime.now()
    then = datetime.datetime(y, m, d, H, M)
    diff = now - then
    return diff

if __name__ == '__main__':
    print uptime()
