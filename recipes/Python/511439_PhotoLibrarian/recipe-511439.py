"""
---------------------------------------------------------------------------------------------------
Filename:       PhotoLibrarian.py
Author:         Alex Harden
Release Date:   2007-03-26
Description:    Iterates through a directory tree, reading the EXIF data from each JPG. Parses the
                date/time from EXIF data, and copies the photo using the date/time value into a
                new camera/year/month-based tree.  Additional sort by day available.
Attributions:   Ideas and code borrowed from Chad Cooper's RenameCopyPhotos.py:
                http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/500266
                EXIF.py: http://sourceforge.net/projects/exif-py/
                Dirwalk.py borrowed from the ActiveState Python Cookbook:
                http://code.activestate.com/recipes/105873/
Changelog:      2007-03-26: Initial 1.0 release.
---------------------------------------------------------------------------------------------------
"""

import string, sys, traceback, datetime, time
import EXIF, os, shutil
import dirwalk

inputDir = 'D:/photos'          #root directory that will be parsed (includes subdirectories)
outputDir = 'D:/photolibrary'   #our output directory (should be present before script is run)
fileExt = '.JPG'                #restrict to JPGs (we need EXIF data)
dateSort = 0                    #additional directory per date? 1=yes, 0=no
pictureList = dirwalk.dirwalk(inputDir)
count = 0

def FilePic(myPicture,myOutputDir,myDateSort):
    """
    Files the specified picture in the OutputDir according to EXIF Camera Model and date:
    /myOutputDir
        /<EXIF Camera Model>
            /<year>
                /<month>
                    /<date>  (optional)
                        /<myPicture>
    """
    # Check for/make dirs for file to go into
    # If dir already exists, use it - if it doesn't exist, then create it

    try:
        f=open(myPicture, 'rb')
        tags=EXIF.process_file(f)
        myFilename=os.path.basename(myPicture)
        datestr = str(tags['EXIF DateTimeDigitized'])
        datestr = datestr.split(' ')
        dt = datestr[0]  # date
        tm = datestr[1]  # time
        # Date
        y = dt.split(':')[0]    # year
       
        if len(dt.split(':')[1]) < 2:   # month
            m = str('0') + dt.split(':')[1] 
        else:
            m = dt.split(':')[1]
           
        if len(dt.split(':')[2]) < 2:   # day
            d = str('0') + dt.split(':')[2] 
        else:
            d = dt.split(':')[2]

        # Time
        h = tm.split(':')[0]  # hour
        min = tm.split(':')[1]  # minute
        s = tm.split(':')[2]  # second

        camera=str(tags['Image Model'])
        if os.path.isdir(myOutputDir + '/' + camera) != 1:
            os.mkdir(myOutputDir + '/' + camera)
        if os.path.isdir(myOutputDir + '/' + camera + '/' + y) != 1:
            os.mkdir(myOutputDir + '/' + camera + '/' + y)
        if os.path.isdir(myOutputDir + '/' + camera + '/' + y + '/' + m) != 1:
            os.mkdir(myOutputDir + '/' + camera + '/' + y + '/' + m)
        if dateSort:
            if os.path.isdir(myOutputDir + '/' + camera + '/' + y + '/' + m + '/' + d) != 1:
                os.mkdir(myOutputDir + '/' + camera + '/' + y + '/' + m + '/' + d)

        # Copy file, renaming it with new filename
        if myDateSort:
            myNewFilePath=myOutputDir + '/' + camera + '/' + y + '/' + m + '/' + d + '/' + myFilename
        else:
            myNewFilePath=myOutputDir + '/' + camera + '/' + y + '/' + m + '/' + myFilename

        print 'New File: %s' % (myNewFilePath)
        shutil.copyfile(myPicture,myNewFilePath)
            
        # Set modified time to date photo was digitized
        myCurrentTime = datetime.datetime.now()
        myCurrentTime = int(time.mktime(myCurrentTime.timetuple()))
        myDigitizedTime = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
        myDigitizedTime = int(time.mktime(myDigitizedTime.timetuple()))
        myTimes=(myCurrentTime,myDigitizedTime)
        os.utime(myNewFilePath,myTimes)
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

def Timer(start, end):
    """
    Calculates the time it takes to run a process, based on start and finish times
    ---------------------------------------------------------------------------------------------
    Inputs:
    start:        Start time of process
    end:          End time of process
    ---------------------------------------------------------------------------------------------
    """
    elapsed = end - start
    # Convert process time, if needed
    if elapsed <= 59:
        time = str(round(elapsed,2)) + " seconds\n"
    if elapsed >= 60 and elapsed <= 3590:
        min = elapsed / 60
        time = str(round(min,2)) + " minutes\n"
    if elapsed >= 3600:
        hour = elapsed / 3600
        time = str(round(hour,2)) + " hours\n"
    return time

##### RUN #####

if __name__ == '__main__':
    start = time.clock()
    for picture in pictureList:
        if string.upper(picture[-4:]) == fileExt:
            FilePic(picture,outputDir,dateSort)                    
            count = count + 1
    finish = time.clock()
    
    print '\nProcessing done in ', Timer(start, finish)
    print 'Images processed: ', str(count)
