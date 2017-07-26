import commands
import os

class singleinstance(object):
    '''
    singleinstance - based on Windows version by Dragan Jovelic this is a Linux
                     version that accomplishes the same task: make sure that
                     only a single instance of an application is running.

    '''
                        
    def __init__(self, pidPath):
        '''
        pidPath - full path/filename where pid for running application is to be
                  stored.  Often this is ./var/<pgmname>.pid
        '''
        self.pidPath=pidPath
        #
        # See if pidFile exists
        #
        if os.path.exists(pidPath):
            #
            # Make sure it is not a "stale" pidFile
            #
            pid=open(pidPath, 'r').read().strip()
            #
            # Check list of running pids, if not running it is stale so
            # overwrite
            #
            pidRunning=commands.getoutput('ls /proc | grep %s' % pid)
            if pidRunning:
                self.lasterror=True

            else:
                self.lasterror=False

        else:
            self.lasterror=False

        if not self.lasterror:
            #
            # Write my pid into pidFile to keep multiple copies of program from
            # running.
            #
            fp=open(pidPath, 'w')
            fp.write(str(os.getpid()))
            fp.close()

    def alreadyrunning(self):
        return self.lasterror

    def __del__(self):
        if not self.lasterror:
            os.unlink(self.pidPath)

if __name__ == "__main__":
    #
    # do this at beginnig of your application
    #
    myapp = singleinstance()
    #
    # check is another instance of same program running
    #
    if myapp.alreadyrunning():
        sys.exit("Another instance of this program is already running")
        
    #
    # not running, safe to continue...
    #
    print "No another instance is running, can continue here"
