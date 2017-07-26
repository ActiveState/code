'''
A simple python script to find out the .NET framework versions 
installed on a local or remote machine. (remote machine does not work yet ;)

Usage:
    donet.py [--machine|-m=<computer_name>] [--check|-c=all|1.0|1.1|2.0|3.0|3.5|4]
    if invoked with a 32 bit python, 32 bit versions of .net framework will be returned;
    if invoked with a 64 bit python, 64 bit versions of .net framework will be returned.

Sample Run:
    C:\IronPythonPlay>'C:\Program Files (x86)\IronPython 2.7.1\ipy64.exe' dotnet.py
    
    2.0.50727.5420     SP2  -     None
    3.0.30729.5420     SP2  -     None
    3.5.30729.5420     SP1  64bit C:\Windows\Microsoft.NET\Framework64\v3.5\ 
    4.0.30319:Client   GA   64bit C:\Windows\Microsoft.NET\Framework64\v4.0.30319\ 
    4.0.30319:Full     GA   64bit c:\Windows\Microsoft.NET\Framework64\v4.0.30319\ 
    
    C:\IronPythonPlay>"C:\Program Files (x86)\IronPython 2.7.1\ipy.exe" dotnet.py 
    
    2.0.50727.5420     SP2  -     None
    3.0.30729.5420     SP2  -     None
    3.5.30729.5420     SP1  32bit C:\Windows\Microsoft.NET\Framework\v3.5\ 
    4.0.30319:Client   GA   32bit C:\Windows\Microsoft.NET\Framework\v4.0.30319\  
    4.0.30319:Full     GA   32bit c:\Windows\Microsoft.NET\Framework\v4.0.30319\ 

Author: Yong Zhao (zonplm At gmail dot com)
Date:   2012-05-22
Rev:    0.1      
'''
import json
import os
import sys

try:
    from _winreg import *
except:
    print '''Unable to import _winreg module!
Please Check your python installation.
'''
    exit(-1)

DOT_NET_VERSIONS = {
    '1.0': (r'Software\Microsoft\Active Setup\Installed Components\{78705f0d-e8db-4b2d-8193-982bdda15ecd}',
            #1.0 Windows XP Media Center 2002/2004/2005 and Tablet PC 2004/2005
            r'Software\Microsoft\Active Setup\Installed Components\{FDC11A6F-17D1-48f9-9EA3-9051954BAA24}'
           ),
    '1.1': (r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v1.1.4322', ),
    '2.0': (r'Software\Microsoft\NET Framework Setup\NDP\v2.0.50727', ),
    '3.0': (r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v3.0',),
    '3.5': (r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v3.5',),
    '4':   (r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Client',
            r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full') # v4 has Client or Full profiles
    # add future .NET framework info below
}

class DotNetVersion(object):
    def __init__(self, version, sp, is32or64, installpath):
        self.version = version
        self.servicepack = sp
        self.is32or64 = is32or64
        self.installpath = installpath
        
    def __repr__(self):
        return json.dumps( {'dotnetversion': self.version,
                             'servicepack': self.servicepack,
                             'is32or64': self.is32or64,
                             'installpath': self.installpath})
        
    def __str__(self):
        sp = 'GA'
        if self.servicepack:
            sp = 'SP'+ str(self.servicepack)
            
        return "{0:18} {1:<4} {2:5} {3}".format(self.version, sp,
                                                self.is32or64,self.installpath)
            
class DotNetManager(object):
    def __init__(self, machine=None):
        try:
            if machine == None:
                self.lm_hive = OpenKey(HKEY_LOCAL_MACHINE, '')
            else:
                self.lm_hive = ConnectRegistry(machine, HKEY_LOCAL_MACHINE)
                
        except WindowsError, ex:
            print ex
            exit(-2)
    
    def __del__(self):
        if self.lm_hive:
            CloseKey(self.lm_hive)
    
    def _getdotnetinfo(self, subkeyname):
        thever = None
        try:
            if subkeyname:
                subkey = OpenKey(self.lm_hive, subkeyname)
                install, itype = QueryValueEx(subkey, 'Install')
                version, vtype = QueryValueEx(subkey, 'Version')
                sp, sptype = QueryValueEx(subkey, 'SP')
                installPath, iptype = QueryValueEx(subkey, 'InstallPath')
                is32or64 = '-'
                if installPath and installPath.find('Framework64') > -1:
                    is32or64 = '64bit'
                elif installPath and installPath.find('Framework') > -1:
                    is32or64 = '32bit'
                    
            if install:
                thever = DotNetVersion(version, sp, is32or64, installPath)
                
            if subkey: CloseKey(subkey)
            
        except Exception, ex:
            #print ex
            pass
            
        return thever
        
    def getdotnetversion(self, iver):
        '''
        Given a version string such as 3.0, return a list of DotNetVersion object
        '''
        thever = None
        allProfile = []
      
        for subkeyname in DOT_NET_VERSIONS.get(iver, []):
            theVer = self._getdotnetinfo(subkeyname)
            #1.0, return as soon as find a valid installation
            if iver == "1.0":
                if theVer: 
                    allProfile.append(theVer)
                    break
            #4, return both Client and Full profiles
            elif iver == "4":
                profile = subkeyname.split("\\")[-1]
                theVer.version += ":"+ profile
          
            if theVer: allProfile.append(theVer)
              
        return allProfile
        #return DotNetVersion('v'+ iver, '0', '32bit', r'C:\dummy\path\v' + iver)
        
    
    def getalldotnetversions(self):
        '''
        Get all .net framework versions installed on the given MACHINE.
        A list of DotNetVersion objects is returned
        '''
        allversions = []
        for ver in DOT_NET_VERSIONS.keys():
            allversions.extend(self.getdotnetversion(ver) )
            
        return allversions

if __name__ == "__main__":
    import argparse
    import pprint
    
    parser = argparse.ArgumentParser(description=
    '''find .NET framework versions installed on MACHINE.
    for now, the script only works on the local machine.
    ''')
    parser.add_argument("-m", "--machine")
    parser.add_argument("-c", "--check", default="all", 
                help=".net versions to check: all|1.0|1.1|2.0|3.0|3.5|4")
    
    args = parser.parse_args()
    
    #for now we just ignore remote machine option
    #pprint.pprint(DOT_NET_VERSIONS)
    if args.machine:
        args.machine = r"\\" + args.machine
    
    if args.machine == None:
        print os.environ['COMPUTERNAME'], ':'
    else:
        print args.machine, ":"
        
    dotnetmgr = DotNetManager(args.machine)
    if (args.check == "all"):
        allvers = dotnetmgr.getalldotnetversions()
        #pprint.pprint(allvers)
    else:
        allvers = dotnetmgr.getdotnetversion(args.check)
    
    for ver in sorted(allvers, lambda x,y: cmp(x.version, y.version)):
            print str(ver)
    
    exit(0)    
    #sys.stdin.readline()
    
    
    
    
    
    
    
