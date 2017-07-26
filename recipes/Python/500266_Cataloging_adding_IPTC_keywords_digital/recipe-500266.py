"""
---------------------------------------------------------------------------------------------------
Filename:       RenameCopyPhotos.py
Author:         Chad Cooper
Date:           2006-09-11
Description:    Iterates through a directory, reading the EXIF data from each jpg. Parses the
                date/time and focal length from EXIF data, renames the photo using the date/time
                and focal length. Copies photo to a directory based on the date, ie 2006/09/11.
                Adds date-related keywords to photo, determines by-line based on camera used, adds
                average RGB code of image as a tuple keyword.

Changelog:      2006-09-11: Script finalized and out of testing.
                2007-01-10: Everything wrapped into functions. Functions for adding by-line and
                date info keywords added.
                2007-01-18: Added error handling to all functions and added Timer() function
---------------------------------------------------------------------------------------------------
"""

import string, time, sys, calendar, Image, traceback
from time import localtime, strftime
from IPTC import IPTCInfo
import EXIF, os, shutil
 
base = '/Users/chad/Pictures/testing'  # base dir 
rawFolder = '/Users/chad/Pictures/exifImport'  # dir where raw images from camera await import
fileExt = '.JPG'
filelist = os.listdir(rawFolder)
count = 0

def RenameFile(base, filename, rawFolder):
    """
    Grabs EXIF tags and renames file based on DateTimeDigitized tag info
    --------------------------------------------------------------------------
    Inputs:
    base:        Base directory for photos --> '/Users/chad/Pictures/testing'
    filename:    Old filename of raw file from camera --> 'DSC_0001.jpg'
    rawFolder:   Temp directory where images are transferred to from camera
    --------------------------------------------------------------------------    
    """
    print 'Original filename: ', filename
    try:
        picNumber = filename[len(filename)-8:len(filename)-4]
        
        # Open file, get EXIF tags, get date string and focal length
        os.chdir(rawFolder)
        f = open(filename, 'rb')
        tags = EXIF.process_file(f)
        datestr = str(tags['EXIF DateTimeDigitized'])
        focalLen = str(tags['EXIF FocalLength'])
       
        # Start parsing EXIF tags we just grabbed
        datestr = datestr.split(' ')
        dt = datestr[0]  # date
        tm = datestr[1]  # time
        
        # Date
        y = dt.split(':')[0]  # year
       
        if len(dt.split(':')[1]) < 2:  # month
            m = str('0') + dt.split(':')[1] 
        else:
            m = dt.split(':')[1]
           
        if len(dt.split(':')[2]) < 2:  # day
            d = str('0') + dt.split(':')[2] 
        else:
            d = dt.split(':')[2]
        
        # Time
        if int(tm.split(':')[0]) < 13:   # hour
            hr = tm.split(':')[0]
            ampm = 'AM'
        elif int(tm.split(':')[0]) > 12:
            hr = (int(tm.split(':')[0]) - 12)
            ampm = 'PM'
            
        min = tm.split(':')[1]   #  minute
        sec = tm.split(':')[2]   #  second
    
        # Establish new filename in form of:
        # 0000_yyyy-mm-dd_hh-mm-ss_00mm.jpg
        newName = picNumber + '_' + dt.replace(':', '-') + '_' + tm.replace(':', '-') + '_' + focalLen + 'mm.jpg'
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
    
    FilePic(rawFolder, base, filename, newName, y, m, d)
    AddDateInfoKeywords(rawFolder, filename, base, newName, y, m, d, hr, ampm)
    WriteByLine(base, newName, y, m, d)
    
def FilePic(rawFolder, base, filename, newName, y, m, d): 
    """
    Files the input image according to date taken --> 2006/07/09
    /Users
      /Chad
        /Pictures
          /2006
            /07
              /09
                image goes here
    --------------------------------------------------------------------------
    Inputs:
    rawFolder:   Temp directory where images are transferred to from camera
    base:        Base directory for photos --> '/Users/chad/Pictures/testing'
    filename:    Old filename of raw file from camera --> 'DSC_0001.jpg'
    newName :    New filename as result of RenameFile --> 0000_yyyy-mm-dd_hh-mm-ss_00mm.jpg
    y:           Year from DateTimeDigitized Exif tag
    m:           Month from DateTimeDigitized Exif tag
    d:           Day from DateTimeDigitized Exif tag
    --------------------------------------------------------------------------    
    """
    # Check for/make dirs for file to go into
    # If dir already exists, use it - if it doesn't exist, then create it
    try:
        if os.path.isdir(base + '/' + y) != 1:
            os.mkdir(base + '/' + y)
        if os.path.isdir(base + '/' + y + '/' + m) != 1:
            os.mkdir(base + '/' + y + '/' + m)
        if os.path.isdir(base + '/' + y + '/' + m + '/' + d) != 1:
            os.mkdir(base + '/' + y + '/' + m + '/' + d)
        # Copy file, renaming it with new filename
        shutil.copyfile(rawFolder + '/' + filename, base + '/' + y + '/' + m + '/' + d + '/' + newName)
        imageName = base + '/' + y + '/' + m + '/' + d + '/' + newName
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
    print 'New home: ', imageName, '\n'
    
def WriteByLine(base, newName, y, m, d):
    """
    Writes author info to the IPTC metadata of jpeg. Does test on original filename
    to see which camera it came from, if Nikon, I took it with my D70; if HP, 
    Will took it with his camera
    --------------------------------------------------------------------------
    Inputs:
    base:        Base directory for photos --> '/Users/chad/Pictures/testing'
    newName :    New filename as result of RenameFile --> 0000_yyyy-mm-dd_hh-mm-ss_00mm.jpg
    y:           Year from DateTimeDigitized Exif tag
    m:           Month from DateTimeDigitized Exif tag
    d:           Day from DateTimeDigitized Exif tag
    --------------------------------------------------------------------------    
    """
    try:
        info = IPTCInfo(os.path.join(base, y, m, d, newName))
        # Test to see who took the pic, depending on the camera
        if filename[:2] == 'HP':
            info.data['by-line'] = 'William L.R. Booher'
            info.data['keywords'] = ['taken by will']
        elif filename[:3] == 'DSC':
            info.data['by-line'] = 'Chad D. Cooper'
        else:
            info.data['by-line'] = ''
        info.saveAs(os.path.join(base, y, m, d, newName))
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

def AddDateInfoKeywords(rawFolder, filename, base, newName, y, m, d, hr, ampm):
    """
    Adds keywords for year, month, and date image was take to jpegs
    Date data acquired from EXIF via exif.py module
    Adds them as a list appendage, as in:
        info.keyword.extend(['y'+y, 'm'+m, 'd'+d, dd])
    --------------------------------------------------------------------------
    Inputs:
    base:        Base directory for photos --> '/Users/chad/Pictures/testing'
    newName :    New filename as result of RenameFile --> 0000_yyyy-mm-dd_hh-mm-ss_00mm.jpg
    y:           Year from DateTimeDigitized Exif tag
    m:           Month from DateTimeDigitized Exif tag
    d:           Day from DateTimeDigitized Exif tag
    --------------------------------------------------------------------------
    """
    try:
        info = IPTCInfo(os.path.join(base, y, m, d, newName))
        # Day of week
        y = int(y)
        m = int(m)
        d = int(d)
        dd = calendar.weekday(y, m, d)
        dict = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',
                5:'Saturday',6:'Sunday'}
        day = dict[dd]
        # Friendly time of day
        tod = TimeOfDay(hr, ampm)
        # Average RGB value of pic
        rgb = 'rgb' + str(GetRgb(rawFolder, filename))
        # Write our keywords to image
        info.keywords.extend(['y' + str(y), 'm' + str(m), 'd' + str(d), day, ampm, tod, rgb])
        info.saveAs(os.path.join(base, str(y), str(m), str(d), newName))
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

def TimeOfDay(hour, ampm):
    """
    From 24 hour time, take the hour and create a human-friendly tag telling us what period
    of the day the photo was taken. Adapted from Dunstan Orchards PHP function at:
    http://1976design.com/blog/archive/2004/07/23/redesign-time-presentation/
    --------------------------------------------------------------------------
    Inputs:
    hour:        Hour, in 24-hour format, our pic was shot
    --------------------------------------------------------------------------    
    """
    try:
        if ampm == 'PM':
            hour = int(hour) + 12
        else:
            hour = int(hour)
        # Get our human-friendly time of day
        if hour < 4:
            tod = 'the wee hours'
        elif hour >= 4 and hour <= 6:
            tod = 'terribly early in the morning'
        elif hour >=7 and hour <= 9:
            tod = 'early morning'
        elif hour == 10:
            tod = 'mid-morning'
        elif hour == 11:
            tod = 'late morning'
        elif hour ==12:
            tod = 'noon hour'
        elif hour >= 13 and hour <= 14:
            tod = 'early afternoon'
        elif hour >= 15 and hour <= 16:
            tod = 'mid=afternoon'
        elif hour == 17:
            tod = 'late afternoon'
        elif hour >= 18 and hour <= 19:
            tod = 'early evening'
        elif hour >= 20 and hour <= 21:
            tod = 'evening time'
        elif hour == 22:
            tod = 'late evening'
        elif hour == 23:
            tod = 'late at night'
        else:
            tod = ''
        return tod
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

def GetRgb(rawFolder, filename):
    """
    Resizes the image down to one pixel in size, then returns a tuple of the 
    RGB values of that pixel. Gives an average RGB value for our image. Might
    be good for something one day.
    ---------------------------------------------------------------------------------------------
    Inputs:
    rawFolder:    Folder where our raw imported files are
    filename:     Image we are processing
    ---------------------------------------------------------------------------------------------
    """
    try:
        i=Image.open(os.path.join(rawFolder, filename))
        rgb = i.quantize(1).convert('RGB').getpixel((0, 0))    
        return rgb
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

##### RUN #####

if __name__ == '__main__':
    start = time.clock()
    for file in filelist:
        filename = os.path.basename(file)
        if filename[-4:] == fileExt:
            RenameFile(base, filename, rawFolder)                    
            count = count + 1
    finish = time.clock()
    
    print '\nProcessing done in ', Timer(start, finish)
    print 'Images processed: ', str(count)
