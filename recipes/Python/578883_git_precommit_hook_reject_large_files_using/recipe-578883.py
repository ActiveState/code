albertjan@debian ~/Desktop/test_repo $ git config --global init.templatedir ~/Desktop/git_template_dir
albertjan@debian ~/Desktop/test_repo $ cd ~/Desktop/git_template_dir
albertjan@debian ~/Desktop/git_template_dir $ cat hooks/pre-commit
#!/usr/bin/python
#-*- mode: python -*-

"""Git pre-commit hook: reject large files, save as 'pre-commit' (no .py) 
and place in .git/hooks"""

__author__  = "Albert-Jan Roskam"
__email__   = "@".join(["fomcl", "yahoo" + ".com"])
__version__ = "1.0.5"

import sys
import os
import re
from subprocess import Popen, PIPE
import StringIO

def git_filesize_hook(megabytes_cutoff=5, verbose=False):
    """Git pre-commit hook: Return error if the maximum file size in the HEAD
    revision exceeds <megabytes_cutoff>, succes (0) otherwise. You can bypass 
    this hook by specifying '--no-verify' as an option in 'git commit'."""
    if verbose: print os.getcwd()

    cmd = "git diff --name-only --cached"
    kwargs = dict(args=cmd, shell=True, stdout=PIPE, cwd=os.getcwd())
    if sys.platform.startswith("win"):
        del kwargs["cwd"]
        cmd = "pushd \"%s\" && " % os.getcwd() + cmd + " && popd"
        kwargs["args"] = cmd
        
    git = Popen(**kwargs)
    output = git.stdout.readlines()
    def try_getsize(f):
        """in case the file is removed with git rm"""
        try:
            return os.path.getsize(f)
        except (EnvironmentError, OSError):
            return 0 
    files = {f.rstrip(): try_getsize(f.strip()) for f in output}
    bytes_cut_off = megabytes_cutoff * 2 ** 20

    too_big = [f for f, size in files.items() if size > bytes_cut_off] 
    if too_big:
        msg = ("ERROR: your commit contains %s files that exceed size "
               "limit of %d bytes:\n%s")
        msg = msg % (len(too_big), bytes_cut_off, "\n".join(sorted(too_big)))
        msg += "\n\nUse the '--no-verify' option to by-pass this hook"
        return msg
    return 0

if __name__ == "__main__":
    sys.exit(git_filesize_hook(0.000001, True))

albertjan@debian ~/Desktop/git_template_dir $ cd -
/home/albertjan/Desktop/test_repo
albertjan@debian ~/Desktop/test_repo $ git init  ## this also fetches my own pre-commit hook from template_dir
Initialized empty Git repository in /home/albertjan/Desktop/test_repo/.git/
albertjan@debian ~/Desktop/test_repo $ touch foo.txt
albertjan@debian ~/Desktop/test_repo $ git add foo.txt
albertjan@debian ~/Desktop/test_repo $ ls -l .git/hooks
total 4
-rw-r--r-- 1 albertjan albertjan 1468 May 22 14:49 pre-commit
albertjan@debian ~/Desktop/test_repo $ git commit -a -m "commit"   ##### hook does not yet work
[master (root-commit) dc82f3d] commit
 0 files changed
 create mode 100644 foo.txt
albertjan@debian
~/Desktop/test_repo $ chmod +x .git/hooks/pre-commit
albertjan@debian ~/Desktop/test_repo $ echo "blaah\n" >> foo.txt
albertjan@debian ~/Desktop/test_repo $ git commit -a -m "commit"  ##### now the hook does its job
/home/albertjan/Desktop/test_repo
ERROR: your commit contains 1 files that exceed size limit of 1 bytes:
foo.txt

Use the '--no-verify' option to by-pass this hook
