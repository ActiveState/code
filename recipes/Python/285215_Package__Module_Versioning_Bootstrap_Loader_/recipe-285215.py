===== [versioner.py] =============================== START ===========
"""
Versioner [v%s] - The ModuleVersioning Bootstrap Loader Manager

Clayton Brown DigitalRUM 2004  e:[python-aspn-at-claytonbrown-dot-net]
---------------------------------------------------------------------------------------------------------------------------
This packages walks a path supplied, installing :
   a. empty __init__.py's - when none exist at all
   b. autoloader __init__.py's - when folder contains no __init__.py, but a script with same name as folder eg: newmodule/newmodule.py
           - note: auto loaders are just __init__.py's with the line 'from newmodule import *' given the above example
   c. version_loader __init__.py's - bootstrap loader to allow python package versioning, dependancy specification @ time of import

   version_loader.py takes care of the rest. (provides requires() for python version, package version, and platform.)   

Dependancies:
   version_loader.py (bootstrap loader to control package versioning)
---------------------------------------------------------------------------------------------------------------------------
 
Usage:
    python versioner.py [-options] [path=currentWorkingDir]

Options:
    -debug         -flag to switch debug on   
    -watch etc,..  -csv list of packages to watch debug output for
    -path          -path to versionise.
    -x             -perform actions (copy/delete/etc) otherwise output will just print what it will do
"""

import os
import sys
import shutil

__version__ = '0.1.0'
versionLoader = os.getcwd() + '/' + 'version_loader.py'
_safePrevented = "--- Safe Mode Prevented: "
_execute = 0                                            #whether to execute commands which will modify file system

def getopts():
    """Returns a dictionary of system arguments, all keys are lowercase
    """
    opts = {}
    i = 1 #position 0 = script name
    while i < len(sys.argv):
        key = str(sys.argv[i])
        try: value = str(sys.argv[i+1])
        except: value = None
        if key.startswith('-'): #if its a flag
            if value and not(value.startswith('-')):
                opts[str(key[1:]).lower()] = value #if it has a value also
                i +=1 #advance cursor passed value
            else:
                opts[key[1:]] = None
        i +=1 #advance cursor passed key
    return opts

def rm(file):#os independant file delete/sets permission bits etc/ os.remove doesn't handle this WTF?
    if os.path.isfile(file):
        if _execute:
            os.chmod( file, os.W_OK)
            if sys.platform == "win32": os.popen( 'attrib -r -a -s -h "%s"' % ( file.replace('/','\\') ) ) #waste windows file attributes
            try: os.remove(file)
            except: return 0
            return 1
        else:
            print _safePrevented + "Remove: " +  file
    else:
        print 'File not found: %s' % (file)
        return 0
    
def populateDirectories(arg,dirname,names):
    for file in names:
        _thisCheck = os.path.join(dirname, file)
        if os.path.isdir(_thisCheck): directories.append(_thisCheck)           
  
def recurseTree(source):    
    if len(source) > 0:            
        os.path.walk(source,populateDirectories,0)

def installVersioning():
    _lastPackage = None
    global _execute
    if _execute: print 'Execution is ON'
    else: print 'Execution is OFF'
    for _dir in directories:
        _dir = str(_dir).replace('\\','/')
        _dirs = _dir.split('/') #create a tuple from path compenents
        _parent_dir = _dir.replace('/' + _dirs[-1],'')
        _thisPackage = _dirs[-2]
        _loader = _parent_dir + "/__init__.py"
        _initfile = _dir + "/__init__.py"
        _checkPackageScript = "%s/%s.py" % ( _dir, _thisPackage )
        _debug = _thisPackage in watchlist or len(watchlist) == 0
        if _globalDebug: _debug = 1
        if not(os.path.isfile( _initfile )): #ensure basic __init__.py's exist
            _initContents = '' #standard place holder __init__.py / no import
            if _debug: print "_checkPackageScript: ", _checkPackageScript
            if os.path.isfile( _checkPackageScript ): #folder name is same as script name
                _initContents = 'from %s import *' % (_thisPackage) #make a auto importer __init__.py to import * from script
                if _debug: print "_initContents: ", _initContents
                if _debug: print 'It seems the package %s needs an auto importer' % _dir
            f = open(_initfile,'wb').write( _initContents )
            if _debug: print '\nInit file created [%s] : %s' % (os.path.isfile(_initfile), _initfile)

        _package, _vPackage = _dirs[-2], str(_dirs[-1]).split('_')
        if _package.startswith('_'): print "WARN!! bad package: '_name': %s\t-- (Package name starts with underscore)" % (_dir)
        if _dirs[-1].startswith(_package):
            if not(_package ==  _vPackage[0] and len(_vPackage) > 1):
                if _debug: print '\nRepeating folders not versioned packages/modules: %s' % (_dir) #do nothing
            else:
                if not( _package == _lastPackage ):
                    if _debug: print '\nVersioning Detected:\n[%s]: %s' % ( _package,_dir )
                    _lastPackage = _package
                    if not(os.path.isfile(_loader)): #install version loader
                        if _execute:
                            try: print '--> Version loader installed [%s]: %s' % (shutil.copy2(versionLoader,_loader), _loader)
                            except Exception, e: print e
                        else:
                            print _safePrevented + "--> Install '%s' --to--> '%s'" % (versionLoader, _loader)
                    else:
                        _thisLoaderTime, _masterLoaderTime = os.path.getmtime(_loader), os.path.getmtime(versionLoader) #get modified times
                        if _masterLoaderTime > _thisLoaderTime: #update version loader if master is newer                            
                            rm(_loader)
                            if _execute:
                                try: print '--> Updated version_loader [%s]: %s' % (shutil.copy2(versionLoader,_loader), _loader)
                                except Exception, e: print e
                            else:
                                print _safePrevented + "Update '%s' --to--> '%s'" % (versionLoader, _loader)
                else:
                    if _debug: print '[%s]: %s' % (_package,_dir)
        
def main(rootDir=None):
    print "Recursing site-packages: [%s]" % ( rootDir )
    if os.path.isdir(rootDir): recurseTree(rootDir)
    else: recurseTree(os.getcwd()) #build a list of all directories within site-packages    
    directories.sort() #sort
    print "Found [%s] paths to inspect" % ( len(directories) )
    installVersioning()
    
if __name__ == "__main__":
    global _globalDebug, _execute, watchlist, directories
    directories = []                                         #list of directories to inspect for versioning etc.
    watchlist = []                                           #list of packages to output debug info for
    _globalDebug = 0                                        #whether to print debug info    
    print "\n\nVersioner.py [v%s]\n--------------------------------" % __version__
    opts = getopts() # get command line options
    directoryToInspect = os.getcwd()
    ## Check flag options
    if len(opts.keys()) > 0:
        if opts.has_key('x'):
            _execute = 1
            print 'Execute is: ON'
        else: print 'Execute is: OFF - safe mode'
        if opts.has_key('debug'):
            _globalDebug = 1
            print 'Full debug: ON'
        else: print 'Debug: OFF'
        if opts.has_key('watch'):
            _debug = watchlist = str(opts['w']).split(',')
            print 'Watch packages [%s] set to: %s' % ( len(watchlist), watchlist )
        if opts.has_key('path'):
            directoryToInspect = opts['p']
            print "Directory to inspect set to: %s" % (directoryToInspect)
        main( directoryToInspect ) #start in current directory
        print "\n------------END-----------------\n"
    else:
        print __doc__ % ( __version__ )

===== [versioner.py] =============================== END ============


===== [version_loader.py] ========================== START ===========
"""
ModuleVersioning Bootstrap Loader

Clayton Brown - DigitalRUM, 2004  e:[python-aspn-at-claytonbrown-dot-net]
Initial code sourced from: a David Ascher, dicussion
http://mail.python.org/pipermail/distutils-sig/1999-April/000262.html

Dependancies:
    versioner.py (manages distrobution of this within versioning directories in site-packages
"""

##Imports 
import sys
import os
import imp
import shutil

##Globals 
__version__ = '0.1.0'
__revision__ = '$Revision: #13 $'
__credits__ = ['Clayton Brown', 'David Ascher', 'Guido van Rossum'] #well he did give birth to Python so some credit due....
__created__ = '2004/05/20'
__modified__ = '$Date: 2004/06/01 $'
_debug = 0
_versionChars = list('1234567890_') #allowable characters in versioning
_versionExample = 'MajorVersion.MinorVersion.PatchVersion.MinorPatch.MinorMinorPatch' #Append further here to extend behaviour levels
_versioningMap = _versionExample.split('.')
_debugKey = '_version_loader_debug_' #declare a variable in your importing script with value = 1 (to display import debug)
_dependenciesFile = 'dependencies'
_platform = None

notes = """===================== Development Notes:  =====================
        $Author: cbrown $
        $Header: //proservices/python/site-packages/python2_2/version_loader.py#13 $
        Added optional "_version_loader_debug_" : outputs debug whilste selecting appropriate package
        Added optional "_platform_" : filter on packages
        Added optional "_package_version_ = '1.1.1.etc'  __closestVersion__ to do partial matches/ complain/raise execptions
        """

usage = "\nVersion_loader.py  [v%s] Usage: use 'python versioner.py' to place within your site-packages where appropriate \n" % ( __version__ ) + \
        "-"*100 + "\nUsage:  (Note: versions can be expressed to pointLevel needed eg '2.2' will allow '2.2.2', '2.2.3' etc)\n (" + \
        "\tInclude _version_loader_debug_ = 0, in your code to disable this debug output\n" + \
        "\tInclude _version_loader_debug_ = 1, in your code to disable usage, yet still display package debug\n" + \
        "\tInclude _foo_version_ = '1.1.1', before import foo, where foo is module your importing & 1.1.1 is compatible version\n" + \
        "\tInclude _python_version_ = '2.2.2', to specify version of PythonInterpreter required \n" + \
        "\tInclude _platform_ = 'platformSuffix', in your code to specify preffered platfrom packages when available\n" + "-"*100 + \
        ""

def stripChars(str, reject=[], accept=[]):
    """Removes specified characters from a string
    
    Passed two lists (accept/reject) this method strip characters out of a string
    """
    if len(str) == 0 or (reject is None and accept is None): return str
    if accept is None: accept = list()
    if reject is None: reject = list()
    count, outstring = 0, ""
    while count < len(str):
        if str[count] in accept and not(str[count] in reject): outstring = outstring + str[count]
        count += 1
    return outstring

def __versionsort__(f1, f2): 
    """sort directory listing in version order
    """
    f1 = stripChars(f1.replace(f1.split('_')[0],''),[], _versionChars )[1:] 
    f2 = stripChars(f2.replace(f2.split('_')[0],''),[], _versionChars )[1:]
    parts1 = f1.split('_')
    parts1[1:] = map(int, parts1)
    parts2 = f2.split('_')
    parts2[1:] = map(int, parts2)
    return cmp(parts1, parts2)

def __closestVersion__(_requiredString,versions,package): 
    """Finds the closes matching version when exact version not available, raises error if requirement cannot be satisfied,
        specifying the depth of the error, eg. Major.Minor.etc.
    
        Some debug output to illustrate wtf is going on.
        Determine best match for 0_5_0 in ['PythonMagick_0_4_0', 'PythonMagick_0_4_9', 'PythonMagick_0_5_0']
        [
            [0, [0, 4, 0], 'PythonMagick_0_4_0', 0],
            [0, [0, 4, 9], 'PythonMagick_0_4_9', 0],
            [0, [0, 5, 0], 'PythonMagick_0_5_0', 0]
        ]
         
        where: [score, [versionDigits], package, errorsDepth] = each item in collection   
    """
    global _debug
    _requiredString = _requiredString.replace('_','.')
    _required = _requiredString.split('.') #convert dotted to underscored / split on underscores
    _tolerance = len( _required )
    if _debug: print '[%s] Determine best match for %s in %s' % (package, _requiredString, versions)
    
    ##Build sortMatrix
    _sortMatrix = []
    for item in versions: 
        _version = item.replace(package + '_','').replace('.','_').split('_') #strip the package prefix
        #for i in range(0,len(_version)): _version[i] = int(_version[i]) #covert to numeric
        #_version = filter(int,_version)#covert to numeric
        _this = [ 0, _version, item ]
        _sortMatrix.append(_this)
        
    ##Iterate sort matrix scoring available packages
    #_required = filter(int,_required)#covert to numeric
    for i in range(0,len(_sortMatrix)): #traverse Matrix giving scores
        j, _stop = 0, 0 #drill into each point performing comparisons
        while j < len(_required) and not(_stop):
            if len(_sortMatrix[i][1]) > j and _sortMatrix[i][1][j] == _required[j]: _sortMatrix[i][0] += 1 #increment score if levelMatch avaliable / found
            else: _stop = 1 #incompatible from here on in
            j += 1 #keep drilling
    
    ##Select best match from sort matrix
    _score, _latest = 0, None 
    for i in range(0,len(_sortMatrix)):#select highest available compatible version, with the highest score
        if _sortMatrix[i][0] >= _score: #if same score but higher version, or higher score
            _score = _sortMatrix[i][0] #Set highscore
            _latest = _sortMatrix[i][2] #Package Name and version
    if _latest and _score >= len( _required ):
        return _latest, _versioningMap[_score]
    else:
        errorDescription = '\n\t[%s v%s] not avaliable: could not find %s \n\tVersion String Example: %s (non integers are stripped)' % ( package, _requiredString, _versioningMap[_score], _versionExample )
        raise Exception, errorDescription

def __isVersioned__(x):
    """Examines directory name to see if appears to be versioned directory
    """
    return x[:len(_thisdir)+1] == _thisdir + '_' #ok lambda could be used here, but frankly it sux and is unreadable later

def __isPlatform__(x):
    """Examines directory name to see if appears to be versioned directory
    """
    return x.lower().endswith(_platform.lower()) #ok lambda could be used here, but frankly it sux and is unreadable later

def __determineVersion__():
    """Check if required '_package_version_' or required '_platform_' has been nominated by callee/importer
    This is variables declared within the importing script, eg:
    _foo_version_ = '1.1.1.1.1' #where the level of points is the level of accuracy required
    _python_version_ = '2.2.2'  #where the level of points is the level of accuracy required
    _platform_ = 'rh3posix'     #where this will be a suffix on the versioned packages available, else falling back on without if none have this
    """
    global _platform, _thisdir
    _versionRequired = '_' + _thisdir + '_version_'
    _listdir = os.listdir(_dir)
    _instdirs = filter(__isVersioned__, _listdir)
    _versionSpecified = None
    try: #get specified platform, and filter packages by this
        _platform = sys._getframe(3).f_globals['_platform_'] 
        if _platform: #reduce versioned packages
            if _debug: print "Platform suffix: %s" % (_platform)
            _instdirstmp = filter(__isPlatform__,_instdirs) #filter available packages by platform
            if len(_instdirstmp) > 0: _instdirs = _instdirstmp #if platform specific packages avaliable, reduce avaliable to these
            elif _debug: print "Platform [%s] specific package not found for [%s]" % ( _platform , _thisdir )
    except: pass
    try:_versionSpecified = stripChars(sys._getframe(3).f_globals[_versionRequired].replace('.', '_'),None, _versionChars )
    except: pass    
    if _debug: print "[%s] Look for: %s  == '%s'" % ( _thisdir, _versionRequired, _versionSpecified )
    if _versionSpecified:  #found a required '_package_version_' in callee   
        _latest = _thisdir + '_' + str(_versionSpecified)
        _exists = os.path.isdir( _dir + '/' + _latest ) #exact version not found        
        if not(_exists): #try and find the closest version
            if _debug: print '[%s] Exact version not found' % (_thisdir)
            _latest, _score = __closestVersion__(_versionSpecified, _instdirs, _thisdir)
            #if _closest: _latest = _closest
            #else: raise Exception, 'Import [%s] not avaliable: could not find %s \nVersion String Example: %s (non integers are stripped)' % ( _thisdir + '_' + _versionSpecified, _score, _versionExample )
    else: #no _package_version_specified so using latest available
        if _debug: print "[%s] _%s_version_ was not specified so using latest package available" % ( _thisdir, _thisdir )
        _instdirs.sort(__versionsort__)
        if _debug: print '[%s] Available: %s' % (_thisdir, _instdirs)
        _latest = _instdirs[-1] #select last version in sorted list
    return _latest

def __init__():
    global _dir, _thisdir, _latest, _debug    
    _dir = __path__[0]
    _thisdir = os.path.basename(_dir)

    _debug, _showUsage = 1, 1
    try: _debugMode = sys._getframe(2).f_globals[_debugKey] #Get debugMode if it has been declared
    except: _debugMode = None   
    if _debugMode == 0: _debug, _showUsage  = 0, 0
    elif _debugMode == 1: _debug, _showUsage = 1, 0
     
    #Determine PythonInterpretor version compatiblity in calling script i.e. look '_python_version_' set in callee and compare with PythonInterpretor Running
    try:     _pythonVersion = sys._getframe(2).f_globals['_python_version_'] 
    except:  _pythonVersion = None
    if _pythonVersion: _pythonOK, _score = __closestVersion__( _pythonVersion, [sys.version.split(' ')[0]], 'PythonInterpretor' ) #compare required python version with this python version
    
    if _debug:
        print '\n'
        if _showUsage: print "Version Loader Debug Mode is on,\n" + usage              
    _latest = __determineVersion__() 
    sys.path.append(_dir.replace('/','\\') + '\\' + _latest) #append the module imported's path to sys.path so build binaries are in path
    if _debug: print '[%s] Selected: [%s]' %  (__path__[0], _latest)

    try:_file, _pathname, _description = imp.find_module(_latest, __path__)#import the determined versioned module
    except Exception, e: print e
    
    _module = imp.load_module(_latest, _file, _pathname, _description) #Load the package now....
    try: _packagePython = _module._python_version_ #check if package nominates a compatible python version
    except: _packagePython = None
    if _packagePython: __closestVersion__( _packagePython, [sys.version.split(' ')[0]], _thisdir + '.PythonInterpretor' ) #compare packages required python version with this python version
    globals().update(_module.__dict__) #update globals

if __name__ == "__main__": print '\n\n' + __doc__ + '\n\n' + usage 
else: __init__()
===== [version_loader.py] ========================== END   ===========
