## Wakeup_With_iTunes.py
## Author:   Joshua Bloom
## Date:     29 January 2006
## Version:  1.0
## Location: http://jbloomdesign.com/blog/2006/01/28/wake-up-with-itunes/
## Copyright (c) 2006, Joshua Bloom
## With thanks to James Thiele http://www.eskimo.com/~jet/python/examples/cmd/ for the console code
import cmd
import os
import pythoncom
import subprocess
import sys
import time
import thread
import win32com.client

class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.playSongBool = False
        self.completekey = None
        self.prompt = "=>> "
        self.intro  = "Welcome to the Itunes wake up console! \n\twake morning_playlist 7:00\nStarts your morning_playlist at 7:00AM\nType help for more command information."

    def do_wake(self,args):
        """Wake starts a song for you. Format is wake playlistname time(24hr) IE wake morningSongs 7:00
        """
        try:
            list = args.split()
            self.playlist = list[0]
            timeVal = list[1]
            splitTime = timeVal.split(":")
            self.hour = splitTime[0]
            self.minute = splitTime[1]
            self.playSongBool = True
            #Check for the named Playlist
            if (self.playListExists(self.playlist)):
                thread.start_new_thread(self.timeChecker,())
            else:
                print ("The playlist %s doesn't exist, your should try one that does" % self.playlist)
        except:
            print"Please format your request correctly: wake playlist time(24hr)"

    def do_cancelwake(self,args):
        """Cancelwake cancels your requested wakeup
        """
        if (self.playSongBool):
            self.playSongBool = False
            self.hour = None
            self.minute = None
            self.song = None
            print("Your wakeup song has been cancelled")
        else:
            print("Nothing currently scheduled so I can't cancel anything.")

    def do_showwake(self,args):
        """Show the Current playlist and Time
        """
        if (self.playSongBool):
            print("Playlist: %s will play at Time: %s:%s" % (self.playlist, self.hour, self.minute))
        else:
            print("Nothing currently scheduled")

    def timeChecker(self):
        while (1):
            if (self.playSongBool and
                int(time.localtime().tm_hour) == int(self.hour) and
                int(time.localtime().tm_min) == int( self.minute) ):
                self.playSong()
            time.sleep(5)

    def playListExists(self, playlistName):
        iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        playlists = iTunes.LibrarySource.Playlists
        numPlaylists = playlists.Count
        while (numPlaylists != 0):
            currPlaylist = playlists.Item(numPlaylists);
            if (currPlaylist.Name == playlistName):
                return True
            numPlaylists -= 1
        return False

    def playSong(self):
        print("Here's your scheduled wakeup! %s " % time.asctime())
        pythoncom.CoInitialize ()
        self.playSongBool = False
        iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        playlists = iTunes.LibrarySource.Playlists
        numPlaylists = playlists.Count
        while (numPlaylists != 0):
            currPlaylist = playlists.Item(numPlaylists);
            if (currPlaylist.Name == self.playlist):
                try:
                    vol = 0
                    iTunes.SoundVolume = vol
                    currPlaylist.PlayFirstTrack()
                    #Ramp Up Volume
                    while (vol < 100):
                        time.sleep(.5)
                        iTunes.SoundVolume = vol
                        vol += 1
                    break
                except:
                    pass
            numPlaylists -= 1

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop (self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

if __name__ == '__main__':
        console = Console()
        console . cmdloop() 
