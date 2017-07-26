#!/usr/bin/env python

import sys
import os
import subprocess
import fnmatch
import rpm

def newest_kernel_and_initrd():
    ts = rpm.TransactionSet()
    p = max(ts.dbMatch('name', 'kernel'))
    k = [ x for x in p['filenames']
         if fnmatch.fnmatch(x, '/boot/vmlinuz-*') ][0]
    #The initrd is not owned by the kernel rpm but generated in the %post script   
    i = '/boot/initrd-%s.img' % k[len('/boot/vmlinuz-'):]
    return (k, i)

def kexec(kernel, initrd, cmdline=None):
    if cmdline == None:
        cmdline = file('/proc/cmdline').read()[:-1] # strip newline
    r = subprocess.call(['/sbin/kexec', '-l', kernel,
                            '--initrd=%s' % initrd,
                            '--command-line=%s' % cmdline])
    if r != 0:
        raise Exception('kexec returned %d' % r)

def program_name():
    return os.path.basename(sys.argv[0])

def main():
    (k, i) = newest_kernel_and_initrd()
    sys.stderr.write('%s: loading ("%s", "%s")\n' % (program_name(), k, i))
    kexec(k, i)
    sys.stderr.write('%s: reboot to load new kernel\n' % program_name())

if __name__ == '__main__':
    main()
