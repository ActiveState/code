#!/usr/bin/env python

import getopt
import sys
import os
import posix
import getpass

# the default root to mount ssh sources
# its a good idea not to place this in ~ directly
DEFAULTMOUNTROOT= os.environ.get ("HOME") + os.sep + "mnt"

class mnt:
    def __init__(self, argv):
        self.read_mountroot_cfg ()
        if not os.path.exists (self.mountroot):
            os.mkdir (self.mountroot)
            print "Creating mountroot in %s" % self.mountroot
        self.argv = argv
        self.uid = os.getuid()
        
    def usage(self, short=True):
        if short:
            print """%s [-u mountpoint] [-p port] [-m mountpoint] <-a|-l|-h|user@host:path>""" % sys.argv[0]
        else:
            print """%s [OPTIONS] SOURCE
        OPTIONS
        -a                            Unmount all sshfs-mounts
        -u <mountpoint>               Unmount mount
        -p <port>                     Use specified port
        -m <mountpoint>               Don't select mountpoint automatically
        -l                            List all mounts
        -h                            This help page
    
        SOURCE is any ssh address. mnt will use the current user if no username
        is given. If the Path is ommitted mnt will mount the home directory.
        Mountpoint is always without directories, see .mntrc
        
        EXAMPLES
        mnt sven@deepblue             
        mnt sven@deepblue:/home
        mnt -m dbroot sven@deepblue:/
        mnt -p 2345 sven@deepblue
        mnt -u deepblue
        mnt -a
        """ % sys.argv[0]

    def _get_mounted_fs (self):
        """ _get_mounted_fs() -> [[source, mountpoint, filesystem, options, p1, p2],...]
        reads mtab and returns a list of mounted sshfs filesystems. """
        try:
            lines = [line.strip("\n").split(" ") for line in open ("/etc/mtab", "r").readlines()]
            return [mount for mount in lines if mount[2]=="fuse.sshfs"]
        except:
            print "Could not read mtab"
        

    def read_mountroot_cfg(self):
        rcfile = os.environ.get ("HOME") + os.sep + ".mntrc"
        if os.path.exists (rcfile):
            try:
                for line in open (rcfile, "r").readlines():
                    if line.startswith ('mountroot='):
                        self.mountroot = line.rsplit ("=")[1].strip("\n")
            except:
                print "Conffile existant but not readable."
        else:
            try:
                self.mountroot = DEFAULTMOUNTROOT
                open (rcfile, "w").writelines ("mountroot=%s" % DEFAULTMOUNTROOT)
                print "Writing default mountroot %s to .mntrc" % DEFAULTMOUNTROOT
            except:
                print "Could not write .mntrc (%s)" % rcfile
    
    def _split_ssh_source (self,source):
        """_split_ssh_source(source) -> (user, host, path)
        split the values of a ssh source, guess the missing parts of user@host:path"""
        try:
            user,hostpart = source.split("@")
        except ValueError:
            user = getpass.getuser()
            try:
                host, path = source.split(":")
            except:
                path = "."
                host = source
        else:
            try:
                host, path = hostpart.split(":")
            except:
                path = "."
                host = hostpart
        return (user, host, path)

    def _get_possible_mountpoint (self, user, host):
        """_get_possible_mountpoint (user, host) -> mountpoint
        guesses a possible free mountpoint and returns it."""
        if not self.mountpoint:
            self.mountpoint = user + "-" + host
        mp = self.mountroot + os.path.sep + self.mountpoint
        return mp

    def do_mount (self,source):
        """do_mount(source)
        mount ssh source as local filesystem by calling sshfs"""
        user, host, path = self._split_ssh_source (source)
        mp = self._get_possible_mountpoint (user, host)
        if not os.path.exists (mp):
            os.mkdir (mp)
        sshfs = "%s@%s:%s" % (user, host, path)
        
        status = os.system ('sshfs -p %d -o uid=%d "%s" "%s"' % (self.port, self.uid, sshfs, mp))
        if status == 0:
           print "%s mounted as %s" % (sshfs, self.mountpoint)
        else:
            os.rmdir (mp)
    
    def do_umount_all(self):
        for src,mp,fs,opts,p1,p2 in self._get_mounted_fs():
            self.do_umount (mp.rsplit (os.path.sep)[-1])
    
    def do_umount (self, mountpoint):
        if os.path.exists (self.mountroot + os.path.sep + mountpoint):
            os.system ("fusermount -u " + self.mountroot + os.path.sep + mountpoint)
            os.rmdir (self.mountroot + os.path.sep + mountpoint)
    
    def do_list(self):
        for src,mp,fs,opts,p1,p2 in self._get_mounted_fs():
            print "%25s mounted on %s" % (src,mp)      
    
    def main(self):
        try:
            opts, args = getopt.getopt(self.argv, "au:lp:m:h", ["all", "unmount", "list", "port", "mountpoint", "help"])            
        except getopt.GetoptError:
            self.usage()
            sys.exit (2)
        
        self.mountpoint=None
        self.port=22
        for opt, arg in opts:
            if opt in ("-u", "--umount"):
                self.do_umount(arg)
                sys.exit(0)
            elif opt in ("-l", "--list"):
                self.do_list()
                sys.exit(0)
            elif opt in ("-h", "--help"):
                self.usage(short=False)
                sys.exit(1)
            elif opt in ("-a", "--all"):
                self.do_umount_all()
                sys.exit(0)
            elif opt in ("-p", "--port"):
                self.port=arg
            elif opt in ("-m", "--mountpoint"):
                self.mountpoint=arg
        self.do_mount (args[0])


if __name__ == '__main__':
    m = mnt(sys.argv[1:])
    m.main()
    
