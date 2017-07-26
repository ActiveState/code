"""
PyOpts.py
Author: AJ Mayorga

A highlevel quick wrapper for simplifying commandline options/arg handling

FEATURES:

    - Generates shorts, longs and help/usage automatically

    - Allows for specification of required options/args or groups there of
      in addition to exclusionary opt/args or groups.

    - Configures default values and selects/"choices" 

    - Returns a simple dictionary with key of supplied key name and value of configured type


DETAILS AND SUCH:

  By passing a dict of args that are normally present & you will use in your code anyway. 
  The arg dict is given a key name & initialize each with its own config dict consisting of
  the following keys and values.
  
  PROJECT KEYS:
  
  About     is an about section that will be used as a header for 
            the generated usage called by -h/--help

  ExitOnErr if True when and error or exception is found in processing the opt/args
            an error message will be generated (if Quiet=False) followed by sys.exit()
  
  Quiet     toggles error/exception message output

  Minimum   the minimum number of required opt/args. This is for trivial commandline 
            requirements. 0 indicates no min required.

  
  All other provided keys are considered option keys the provided names for which will be used
  to derive shorts '-p' and longs '--port'. Each option key's value is initialized with a 
  configuration dict.

  CONFIG DICT:
  
  GID   group identifier for a vars used by REQ  Can be alpha/num value
 
  REQ   indicates variable requirement when not present False is default
          - True indicates an independent value must be supplied, False not necessary
          - When a list of GIDs is supplied the var requirment is True and 
            all group members without a '-' prefix must have asigned values.
            A GID prefixed with a '-' indicates an exclusionary var meaning if 
            if provided with a current var an error will occur (think xor) 

  VALUE  serves as default value and/or type cast reference for final value
         for all variables that are int, strings, bools or float.
            - When a list is provided it serves as a choice selection
              where the provided value must match one listed in the list.
         
  HELP   a short descriptive line that is returned along with an error message
         if an error is discovered related to the var. Also used to construct
         --help/-h usage output

  if all opts/args are received without error the config portion of of the ARGS dict
  is overwritten with the user supplied value cast to the type of the supplied 'VALUE'
  from the orig config.

  opts/args supplied by the user that are not configured are ignored.

  a list of mock debug values can be supplied (see SA below) for debugging providing
  this list overrides reading sys.argv[1:]

  
#####################################################################################################
"""



import sys, os, string

class PyOptsException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

class PyOpts(PyOptsException):
    
    def __init__(self):
        self.SA         = None
        self.about      = '' 
        self.uhead      = ''
        self.ExitOnErr  = False 
        self.Quiet      = False
        self.help       = False   
        self.usage      = []
        self.Temp       = []
        self.Lost       = {}
        self.Groups     = {}
        self.OUT        = {}
        self.Found      = []
        self.Minimum    = 0
        self.Configs    = ['About','Quiet','ExitOnErr','Minimum','Missing']
        
        self.ErrorMsgs  = ['Missing Member: %s of Option Group %s',
                           'Invalid Arguement: %s For Option %s Valid Args Are: %s',
                           'Duplicate Long Name Found Check Key Name In Init Dict',
                           'No Members Assigned To Required Group: ',
                           'Error Missing Required Parameter : %s  %s',
                           '%s Options/Args Less Than Required Minimum %s',
                           'Exclusion Error Option %s Cannot Not Be Used With %s' ]
    
    def OnErr(self, ErrorNum, args):
       if not self.Quiet:
           print self.ErrorMsgs[ErrorNum] % args
       if self.ExitOnErr:
          sys.exit(1)
       return False
        
    def SL(self, v, z):
        d = self.Temp
        if z+v in d:
           if z == '-':
               short = (z+[x for x in string.letters if not z+x in d][0],
                        z+v.upper())[not z+v.upper() in d]
               self.Temp.append(short)
               return short
           raise PyOptsException(self.ErrorMsgs[2])
        long = z+v
        self.Temp.append(long)  
        return long
            
    def CastAs(self, var, varType):
        try:
            if   isinstance(varType, bool): return bool(var)
            elif isinstance(varType, str):  return str(var)
            elif isinstance(varType, int):  return int(var)
            elif isinstance(varType, float):return float(var)
            elif isinstance(varType, long): return long(var)
            elif isinstance(varType, int):  return int(var) 
        except:
            return False    
        
    def GetValue(self, opt,cV,aV):
        val = self.CastAs(aV, cV)
        if not isinstance(cV, list):
            return val
        for x in cV:
            y = self.GetValue(opt,x, aV)
            if repr(y) == repr(x):
                return y
        choices = '|'.join([str(x) for x in cV])
        self.OnErr(1,(repr(aV),opt,choices))
    
    def LookUp(self, d, key):
        for k,v in d.iteritems():
            if k in self.Configs: continue
            if k == key:
                return v
            elif isinstance(d[k], dict):
               r = self.LookUp(d[k], key)
               if r: return r
        return None
                           
    def DependencyCheck(self, Opts):
        for gid, members in self.Groups.iteritems():
            missing = [x for x in members if x not in self.Found]
            self.Groups[gid]['Missing'] = missing
        
        for opt, conf in Opts.iteritems():
           if opt in self.Configs:
               continue
           exclude = False
           if isinstance(conf['REQ'], list):
               for gid in conf['REQ']:
                   if isinstance(gid, int):
                       if gid < 0:
                           exclude=True
                           gid = abs(gid)
                   else:
                       if gid[0] == '-':
                           exclude=True
                           gid = gid.replace('-','')
                   gid = repr(gid)       
                   if self.Groups.has_key(gid):                   
                       groupOpts = repr([x for x in self.Groups[gid].itervalues() if x != []])
                       groupOpts = groupOpts.replace("'", "")
                       
                       if self.Groups[gid] and exclude:
                           opt = repr(self.LookUp(self.Groups, opt)).replace("'","")
                           self.OnErr(6, (opt,groupOpts))
                                      
                       if self.Groups[gid]['Missing'] != []:
                           mia = ''
                           for member in  self.Groups[gid]['Missing']:
                               mia += repr(self.Groups[gid][member]).replace("'","")
                               return mia,groupOpts
                   else:
                       print self.Groups
                       raise PyOptsException(self.ErrorMsgs[3]+gid)
        return False
                   
    def OP(self, Opts, SA=False):
        SA              = (SA,sys.argv[1:])[SA==False] 
        self.about      =  Opts.get('About', '')
        self.ExitOnErr  =  Opts.get('ExitOnErr', True)
        self.Quiet      =  Opts.get('Quiet', False)    
        self.Minimum    =  Opts.get('Minimum', 0)
        
        for opt, conf in Opts.iteritems():
            if opt in self.Configs:
                continue
            
            conf['GID']   = gid   = conf.get('GID', None)
            conf['REQ']   = req   = conf.get('REQ', False)
            conf['HELP']  = help  = conf.get('HELP', '---')
            conf['VALUE'] = value = conf.get('VALUE', '')
            conf['VALUE'] = value = (value,'True/False')[isinstance(value,bool)]
            
            short, long = (self.SL(opt[:1],'-'), self.SL(opt,'--'))
           
            self.usage.extend([' '+short+' '*2,long+' '*(15-len(long)),
                               str(value)+' '*(20-len(str(value))),help,'\n'])

            if gid != None:
                gid = repr(gid)
                if not self.Groups.has_key(gid):
                    self.Groups[gid]={}
                self.Groups[gid][opt] = [short,long]
               
            if not short in SA and not long in SA and req:
                 if gid:
                     self.Lost[gid] = opt
                 if req == True:
                     self.OnErr(4,(opt,help))
            
            for x in range(len(SA)):
                if SA[x] == '-h' or SA[x] == '--help':
                    self.help = True
                    continue
                if SA[x] == long or SA[x] == short:
                    self.OUT[opt] = self.GetValue(opt, value, SA[x+1])
                    self.Found.append(opt)
                        
        if len(self.Found) < self.Minimum:
            self.OnErr(5, (len(self.Found),self.Minimum))
             
        mia = self.DependencyCheck(Opts)
        if mia:
            self.OnErr(0,mia)
                   
        if self.help:
           print self.about+self.uhead+'\n'+''.join(self.usage)
           sys.exit(1)
   
        return self.OUT
    
#------------------------------------------------------------------------------#
# DEMO PROJECT STARTS HERE

from PyOpts import PyOpts


__author__  = "AJ Mayorga"
__version__ = "1.0.1"
__status__  = "Demo"
              
   
ABOUT="""
################################################################################
  project: myOpts.py                                                
                                                                    
  version : """+__version__+"""                                     
  author  : """+__author__+"""
  status  : """+__status__+"""
         
  This is a Demo Program To Illustrate Handling Of Options/Arguments 
  At The Commandline
         
################################################################################
"""
 
#For Debugging Play With These To Override sys.argv[1:] to see how things are handled

SA  = ['myOpts.py','--to','Mary','--fromname','boomers', 
       '--body','blah','--fromaddress', 'Billy@yuckbutt.com',
       '--subject', 'Scooters', '--threads',43, '--template','Monkey','-h'] 

 
class OPTIONS_DEMO:
    
    def __init__(self):
         
         #Simple Option/Args
         
         self.ARGS = {}
         self.ARGS['About']        = ABOUT
         self.ARGS['Minimum']      = 4
         self.ARGS['to']           = {'VALUE': "", 'HELP':"Email List or Single Address"}
         self.ARGS['fromaddress']  = {'VALUE': "", 'HELP':"Email Address of Sender e.g.WB@blah.com"}
         self.ARGS['subject']      = {'VALUE': "", 'HELP':"Subject of Email"}
         self.ARGS['body']         = {'VALUE': "", 'HELP':"Body/Content of Email (File or String)"}         
   
         """
         #Advanced Option/Args
         PROTOS = ["HTTP","HTTPS","FTP"]
         
         self.ARGS = {}
         self.ARGS['About']        = ABOUT
         self.ARGS['ExitOnErr']    = True
         self.ARGS['Quiet']        = False
         self.ARGS['Minimum']      = 0
         
         self.ARGS['newtemplate']  = {'GID':0, 'REQ':[-1],  'VALUE': False, 'HELP':"Save Resulting Email As New Template"}
         self.ARGS['template']     = {'GID':1, 'REQ':[-0],  'VALUE': False, 'HELP':"Email Template To Use"}
         self.ARGS['to']           = {'GID':2, 'REQ':True,  'VALUE': "",    'HELP':"Email List or Single Address"}
         self.ARGS['fromname']     = {'GID':3, 'REQ':[2],   'VALUE': "",    'HELP':"Name of Sender e.g. Will J Buck CEO"}
         self.ARGS['fromaddress']  = {'GID':4, 'REQ':[3],   'VALUE': "",    'HELP':"Email Address of Sender e.g. WB@blah.com"}
         self.ARGS['subject']      = {'GID':5, 'REQ':[4],   'VALUE': "",    'HELP':"Subject of Email"}
         self.ARGS['body']         = {'GID':6, 'REQ':[5],   'VALUE': "",    'HELP':"Body/Content of Email (File or String)"}
         self.ARGS['attachments']  = {         'REQ':False, 'VALUE': "",    'HELP':"Comma Separated List of Attachment Files"}
         self.ARGS['threads']      = {         'REQ':False, 'VALUE': 1,     'HELP':"Number of Sending Threads"}
         self.ARGS['signed']       = {         'REQ':False, 'VALUE': False, 'HELP':"Digitally Sign On Each Sent Email"}
         self.ARGS['readreceipt']  = {         'REQ':False, 'VALUE': False, 'HELP':"Require Read Receipts"}
         self.ARGS['linkprotocol'] = {         'REQ':False, 'VALUE': PROTOS,'HELP':"Format Embedded Links To Protocol"}
         """
         
         self.ARGS = PyOpts().OP(self.ARGS,SA)  
         
         print self.ARGS
    
      
if __name__ == '__main__':
    
    OD = OPTIONS_DEMO()
    
   
