# 09-01-04
#v1.0.1
#

#
# Prints output to the screen and/or
# logs it to a file - depending on the settings.
#
# Prints output to the screen and/or
# logs it to a file - depending on the settings.
#
# To use this function you need to include verbose (yes if you want to print to screen), 'outputpath' (filename)
# ('' if you don't want to output to a file) and 'logmode'( (w)rite or (a)ppend )
#
# If passed in an alternative method for printing (newfunc) it can also output using that method !
# This method can be created at any time.
# Usage :
# verbose = 'Yes' # to print to screen 
# outputpath = 'system/logfile.txt' # logfile to print to, or '' for no logging
# logmode = 'w' # the mode to open the logfile in - 'w' for write or 'a' for append
#
# from standout import StandOut
# stout = StandOut(verbose, outputpath, logmode, newfunc=None)
# stout.out('message line\n') # this line prints to the screen and adds a line to logfile.txt
# stout.close() # closes the logging file
# stout.verbose = 'No' # Switches printing off
# stout.newfunc = printtowindow # sets an additional printing function
# stout.newfile(outputpath, logmode) # sets a file to log to if the object was originally created without one


class StandOut:
    "Creates an output object that will print *and/or* write to an output file if required."
    def __init__(self,verbose,outputpath,logmode, newfunc=None):
        self.verbose=verbose.lower().strip()
        if logmode=='a' and outputpath !='':      # are we appending or creating a newfile ?
            self.outputfile=open(outputpath,'a')
            self.putout('\n\n')
        elif outputpath != '':
            self.outputfile=open(outputpath,'w')
        else:
            self.outputfile=''
        self.newfunc = newfunc

    def out(self,line):
        if self.verbose=='yes':
            print line,
        if self.outputfile:
            self.outputfile.write(line)
        if self.newfunc:
            self.newfunc(line)
            
    def close(self):
        if self.outputfile != '':
            self.outputfile.close()
            self.outputfile = ''

    def newfile(self, outputpath,logmode):
        """Use this method for adding a file after creating the object without one."""
        if logmode=='a' and outputpath !='':      # are we appending or creating a newfile ?
            self.outputfile=open(outputpath,'a')
            self.putout('\n\n')
        elif outputpath != '':
            self.outputfile=open(outputpath,'w')
