import os
import re

def ssh_attach(ssh_agent_cmd):
    sh_cmds=os.popen(ssh_agent_cmd).readlines()
    for sh_line in sh_cmds:
        matches=re.search("(\S+)\=(\S+)\;", sh_line)
        os.environ[matches.group(1)]=matches.group(2)
