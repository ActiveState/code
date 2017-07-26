#/usr/bin/env python
import subprocess

class RunCmd(object):
    def cmd_run(self, cmd):
        self.cmd = cmd
        subprocess.call(self.cmd, shell=True)

#Sample usage

a = RunCmd()
a.cmd_run('ls -l')
