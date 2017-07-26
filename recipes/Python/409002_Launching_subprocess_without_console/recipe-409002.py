import subprocess

def launchWithoutConsole(command, args):
    """Launches 'command' windowless and waits until finished"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen([command] + args, startupinfo=startupinfo).wait()

if __name__ == "__main__":
    # test with "pythonw.exe"
    launchWithoutConsole("d:\\bin\\gzip.exe", ["-d", "myfile.gz"])
