import urllib, os, sys, time, locale
from time import localtime, strftime
locale.setlocale(locale.LC_ALL, '')


##### VARIABLES #####
# Local dir for storage
ldir = 'E:/temp/radar/LZK/N1P/'
# Remote URL base
rurl = 'http://www.srh.noaa.gov/ridge/RadarImg/'
# Timestamp for file rename
stamp = strftime('%m%d%Y_%H%M%S', localtime())


def FetchRidgeImage(url, type, station):
    """
    Fetches RIDGE radar image (.gif) and world file (.gfw) of given image type
    for station at url
    ------------------------------------------------------------------------------
    Inputs:
    url:        Remote URL of directory where images live
    type:       Image type:
                N0R: Base Reflectivity
                N0S: Storm Relative Motion
                N0V: Base Velocity
                N1P: One-Hour Precipitation
                NCR: Composite Reflectivity
                NTP: Storm Total Precipitation
                See http://www.srh.noaa.gov/jetstream/remote/ridge_download.htm for more info
    station:    Radar station ID. See 
                http://www.srh.noaa.gov/jetstream/remote/ridge_download.htm#radar for more info
    ------------------------------------------------------------------------------
    """
    # URL of image(s) we want
    url = [url + type + '/' + station + '_' + type + '_0' + '.gif']
    for base in url:
        # Get the base url
        urlbase = base[:-13]
        for file in url:
            # Get only the file name without extention
            fileonly = file[-13:-4]
            # Set list of extentions for filetypes we want
            list = ['gif', 'gfw']
            # Get all files with extension in list
            for ext in list:
                fullname = fileonly + '.' + ext
                urllib.urlretrieve(urlbase + fullname, ldir + fullname)


def GrabFileToRename(ldir, type, station):
    """
    Grabs our new file(s) and renames them with a timestamp
    ------------------------------------------------------------------------------
    Inputs:
    ldir:        Local directory where images are downloaded to
    type:        Image type (see docstring in FetchRidgeImage)
    station:     Radar station ID (see docstring in FetchRidgeImage)
    ------------------------------------------------------------------------------
    """
    imagelist = [os.path.join(ldir, station + '_' + type + '_0' + '.gif')]
    # Loop thru images we just downloaded (.gif & .gfw), rename them with timestamp
    for imagebase in imagelist:
        imagebase = imagebase[:-13]
        for imgfile in imagelist:
            imgfileonly = imgfile[-13:-4]
            # Set list of extentions
            list = ['gif', 'gfw']
            for imgext in list:
                fullimgname = imgfileonly + '.' + imgext
                # Call rename f(x)
                RenameWithTimeStamp(os.path.join(imagebase, fullimgname),
                    os.path.join(imagebase, imgfileonly + '_' + stamp + '.' + imgext))


def RenameWithTimeStamp(old, new):
    """
    Uses os.rename to change filename to that with timestamp, in order to 
    avoid duplicates
    ------------------------------------------------------------------------------
    Inputs:
    old:        Old file name
    new:        New file name
    ------------------------------------------------------------------------------
    """
    os.rename(old, new)
    
if __name__ == '__main__':
    FetchRidgeImage(rurl, 'N1P', 'LZK')
    GrabFileToRename(ldir, 'N1P', 'LZK')
                
