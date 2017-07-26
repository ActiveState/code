# drive ghoster
# Author: c8
# Description: A program that will create a "ghost" of a given directory or drive on windows systems
# (easily adaptable to unix etc) to a given destination. This will consist of a copy of all folders and files
# with only names and extensions retained, not size.
# This allows browsing of a remote drive or network location when offline.

# sample input:
#   Automatic run, with prompts. ghoster2.py -s SOURCE -d DEST
#   Manual selection of 'l', will show list of changes. ghoster2.py -s SOURCE -d DEST -l
#   Manual selection of 'u', will commit changes. ghoster2.py -s SOURCE -d DEST -u


# imports
import os
import sys
import shutil
import msvcrt
import win32file
import string
import codecs
import argparse
from datetime import datetime

class Ghoster():

    def __init__(self):   
        self.enumerate_drives()
        self.parse_args()
        
        self.truncated = False
        self.ignore_list = ['System Volume Information']
        
        self.sanity_checks()
    

    # determine system drives
    def enumerate_drives(self):
        drives = []
        for i in string.ascii_lowercase:
            t = "%s:\\" % i
            if win32file.GetDriveType(t) == win32file.DRIVE_FIXED:
                drives.extend(t[0])

        self.drive_str = ', '.join(a.upper() for a in drives)            
               

    # arg parser
    def parse_args(self):
        parser = argparse.ArgumentParser(description='Create local 0Kb copy of remote drive or destination')
        parser.add_argument('-l','--log', action="store_true", default=False, dest="log", help='Log run of program')
        parser.add_argument('-u','--update', action="store_true", default=False, dest="update", help='Run and update changes')
        parser.add_argument('-d','--dest', dest="dest", help='Provide destination for ghost copy, for example one \
        of the following connected system drives:\n' + self.drive_str, required = True)
        parser.add_argument('-s','--source', dest="source", help='Provide source location', required = True)
        parser.add_argument('-o','--output', dest="output", help='Log in provided file')

        args = vars(parser.parse_args())

        # require only one (if provided) mode option
        if (args['log'] or args['update']):
            if (args['log'] and args['update']):
                parser.error('Please enter only one action, add --log OR --update')
                exit()
            else:
                self.manual = 'log' if args['log'] else 'update'
        else:
            self.manual = ''
          
            
        # parse destination option
        ghost_drive = args['source'] + ':/' if len(args['source']) == 1 else args['source']
        save_dir = args['dest'] if args['dest'][-1] == '\\' else args['dest'] + '\\'
        
        self.args = args
        self.ghost_drive = unicode(ghost_drive)
        self.save_dir = unicode(save_dir + ghost_drive[0] + '\\')

        # parse output option
        if args['output']:
            self.logging = True
            self.logging_location = args['output']
        else:
            self.logging = False
  
    # safety checks
    def sanity_checks(self):
        # if run on platform that isn't windows
        if os.name != 'nt':
            print 'This program is currently only windows compatible. Sorry!'
            exit()
        
        # if drive not attached
        if not os.path.exists(self.ghost_drive):
            print self.ghost_drive + ' not attached'
            exit()
            
        # disallow c:\ drive
        if self.args['source'] == 'c':
            print "You probably don't want to be ghosting c:/ drive..."
            exit()
            
        # prevent recursive copying
        if self.normalise_backslash(self.args['source']) in self.normalise_backslash(self.args['dest']):
            print 'destination is part of the ghost - please see recursion in a dictionary'
            exit()
            
        # prompt if dest is root
        #if save_dir:    
        if len(self.args['dest']) == 3:
            print "Are you sure that you want to copy to the root of the drive? y/n"
            answer = msvcrt.getch()
            if answer.lower() == 'y':
                pass
            else:
                exit()
  
############################### General Purpose #############################################
    def normalise_backslash(self, inp):
        return inp.replace('/','\\')
      
    # insert commas in numbers (ints and floats)
    def numbers_with_commas(self, number, decimals = 2):
        tail = '.' + str(number).rpartition('.')[-1] if '.' in str(number) else ''
        temp = ''
        for idx, i in enumerate(str(int(number))[::-1]):
            if idx % 3 == 0 and idx != 0 and i != '-':
                temp += ','
            temp += i
        return temp[::-1] + str(tail)[:decimals + 1]  

    # return size in Gb/Mb/Kb/b appropriately as string. 
    # Takes size in bytes.
    def size_normalise(self, size, magnitude = None):
        sizes = {'b':1, 'kb':1024, 'mb':1024**2, 'gb':1024**3, 'tb':1024**4}
        if magnitude:
            magnitude = magnitude.lower()
            if magnitude not in sizes:
                print 'no such size possible, defaulting to Mb'
                magnitude = 'mb'
            size_type = magnitude              
            new_size = float(size) / sizes[magnitude]
        else:
            if size < 1024:
                size_type = 'b'
                new_size = float(size)
            elif size < 1024**2:
                size_type = 'kb'
                new_size = float(size) / 1024
            elif size < 1024**3:
                size_type = 'mb'
                new_size = float(size) / (1024**2)
            elif size < 1024**4:
                size_type = 'gb'
                new_size = float(size) / (1024**3)                
            # Current max of Tb
            else:
                size_type = 'tb'
                new_size = float(size) / (1024**4)
        
        return self.numbers_with_commas(new_size), size_type.title()

##############################################################################################        
        
    # calculate disc size and test for overly large file names    
    def data_enumerate(self, path):
        print "\nCalculating disk size"
        truncate = []
        files = 0
        dirs = 0
        file_size = 0
        prev_dir = ''
        self.trunc_dir_count = 0
        
        for dirname, dirnames, filenames in os.walk(path):
            if dirname.rpartition('\\')[-1] not in self.ignore_list:
                dirs += len(dirnames)
                files += len(filenames)
                
                for a_file in filenames: 
                    file_size += os.path.getsize(os.path.join(dirname,a_file))
                    if len(os.path.join(self.save_dir + dirname[3:], a_file)) > 255:
                        if self.save_dir + dirname[3:] == prev_dir:
                            truncate.append('\t%s' % a_file)
                        else:    
                            self.trunc_dir_count += 1
                            truncate.append(self.save_dir + dirname[3:])
                            truncate.append('\t%s' % a_file)
                            prev_dir = self.save_dir + dirname[3:]
                        
        
        print "%s files and %s directories in dir %s with size %s%s" % ((self.numbers_with_commas(files),) + (self.numbers_with_commas(dirs),) + (self.ghost_drive,) + self.size_normalise(file_size))
        print

        if truncate:
            self.print_limiter(truncate, max_lines = 5, truncate = True)
            truncated = True
        else:
            truncated = False
            
        return files, dirs, truncated

    def update(self, files, dirs, commit_changes = False):  
        changes = []
        completed = {'files':0, 'dirs':0}
        percentage = -5
        
        # else if dest not exist, create
        if commit_changes:        
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)    

        print '[',
        
        # recurse drive: remove files/dir if shouldn't exist, create if should and doesn't
        for dirname, dirnames, filenames in os.walk(self.ghost_drive):
            if dirname.rpartition('\\')[-1] not in self.ignore_list:
                completed['dirs'] += 1
                trunc_dirname = dirname[3:]

                # for each dir...
                if os.path.exists(self.save_dir + trunc_dirname):
                    dirnames_a = os.walk(self.save_dir + trunc_dirname).next()[1]
                    filenames_a = os.walk(self.save_dir + trunc_dirname).next()[2]
                    
                    # if there diff number of files in save dir and source
                    if filenames_a != filenames:
                        # remove old files from save location since deleted 
                        for filename_a in filenames_a:
                            if filename_a not in filenames:
                                path = os.path.join(self.save_dir + trunc_dirname,filename_a)
                                if commit_changes:
                                    os.remove(path)
                                changes.extend(['DELETE: %s' % path])
                    
                        # create any new files in destination            
                        for filename in filenames:
                            if filename not in filenames_a:
                                completed['files'] += 1
                                path = self.save_dir + trunc_dirname
                                        
                                if not os.path.exists(os.path.join(path, filename)):
                                    if commit_changes:
                                        temp = open(os.path.join(path, filename),'w')
                                        temp.close()
                                    changes.extend(['ADD: %s' % os.path.join(path, filename)])
                    
                    # if identical add to completed files
                    else:
                        completed['files'] += len(filenames)
                    
                    # if diff number of dir in save dir and source
                    if dirnames_a != dirnames:
                        for a_dir in dirnames_a:
                            if a_dir not in dirnames:
                                path = os.path.join(self.save_dir,a_dir)
                                if commit_changes:
                                    shutil.rmtree(path)            
                                changes.extend(['ADD: %s' % path])
                                    
                # else folder doesn't exist => create                    
                else:
                    if commit_changes:
                        os.makedirs(self.save_dir + trunc_dirname)
                    changes.extend(['ADD: %s' % self.save_dir + trunc_dirname])
                    
                    # create any new files in destination            
                    for filename in filenames:
                        completed['files'] += 1
                        path = self.save_dir + trunc_dirname
                                
                        if not os.path.exists(os.path.join(path, filename)):
                            if commit_changes:
                                temp = open(os.path.join(path, filename),'w')
                                temp.close()
                            changes.extend(['ADD: %s' % os.path.join(path, filename)])
                                
                # time remaining
                if (float(completed['files']) / files * 100) >= percentage + 5:
                    print ' %d%%' % ((int(float(completed['files']) / files * 100)) / 5 * 5),
                    percentage = (float(completed['files']) / files * 100) /5 * 5

        if percentage != 100:
            print ' 100%',
        print ']'
        
        if commit_changes and changes:
            print '\nAll changes commited.\n'
        elif commit_changes and not changes:
            print '\nThere were no changes to commit.\n'
        elif not changes:
            print '\nThere were no changes.\n'

        return changes

    def logger_printer(self, output, truncate = False):
        if self.logging:
            if truncate:
                print output,
            self.log.write(output)
        else:
            print output,            
                
    # (only) the following can be logged as results may need to be viewed seperately    
    def print_limiter(self, source, commit_changes = False, max_lines = 15, truncate = False, increment = 20):
        if not source:
            return
            
        lines = len(source)
        current_line = 0

        # open log file
        if self.logging:
            self.log = codecs.open(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),self.logging_location) ,'w', "utf-8")  
            self.log.write(datetime.now().strftime('%d-%m-%Y, %H:%M:%S') + '\n')

        if truncate:
            self.logger_printer('\nThe following files will have their name truncated:\n\n', truncate)
        elif commit_changes:
            self.logger_printer('\nThe following changes have been commited:\n\n')
        else:
            self.logger_printer('\nThe following changes will occur:\n\n')

        if lines > max_lines:            
            print "There are %d files and dirs. Do you want to view them all? press 'y' or 'n'" % (lines - self.trunc_dir_count)
            ans = msvcrt.getch()
            if ans == 'y':
                while(current_line < lines):
                    if current_line + increment > lines:
                        upper_limit = lines
                    else:
                        upper_limit = current_line + increment
                    for i in range(current_line, upper_limit):
                        self.logger_printer('%s\n' % source[i], truncate)

                    if i != upper_limit - 1:    
                        print "Press 's' to skip the rest, enter to continue"
                        ans = msvcrt.getch()
                        if ans == 's':
                            break
                    current_line += increment
            elif ans == 'n':
                pass
            else:
                pass
        else:
            for i in source:
                self.logger_printer('%s\n' % i, truncate)
        # close log file        
        if self.logging:
            self.log.close()    


    def auto_run(self, files, dirs):
        while(True):
            print '\nTo show a list of files and dirs to be changed press "l"'
            print 'To update the destination press "u"'
            print 'To quit type q\n'
            
            command = msvcrt.getch()

            if command.lower() == 'l':
                self.run_type(files, dirs, commit_changes = False)
                    
            elif command.lower() == 'u':
                self.update(files, dirs, commit_changes = True)
                break
            elif command.lower() == 'q':
                break
            else:
                pass
    
    def manual_run(self, files, dirs):
        if self.manual == 'update':
            self.run_type(files, dirs, commit_changes = True)
        elif self.manual == 'log':
            self.run_type(files, dirs, commit_changes = False)
    
    def run_type(self, files, dirs, commit_changes):
        changes = self.update(files, dirs, commit_changes)
        self.print_limiter(changes, commit_changes) 

    def execute(self):        
        try:
            # Count files and dirs
            files, dirs, truncated = self.data_enumerate(self.ghost_drive)

            if truncated:
                print "\nPlease correct directory names to prevent file name truncation and rerun"
                exit()
               
            if self.manual:
                self.manual_run(files, dirs)
            else:
                self.auto_run(files, dirs)
            
            print "\nGood Bye"        
        except WindowsError:
            print "WindowsError occured - could the source or destination have been removed mid process?"
            exit()
def main():
    ghoster = Ghoster()
    ghoster.execute()
    
# take it away sam...
if __name__ == '__main__':
    main()
