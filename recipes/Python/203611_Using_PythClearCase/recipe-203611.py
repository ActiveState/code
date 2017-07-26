# CommentPolicy.py - Pre Checkin Trigger 
import os, sys, re, tkMessageBox 
 
def checkComment(comment): 
    comment = comment.lower() 
    caseIds = re.findall(r'bug\d+|feat\d+',comment) 
    return caseIds 
 
def main(): 
    comment = os.environ.get('CLEARCASE_COMMENT','') 
    version = os.environ['CLEARCASE_XPN'] 
 
    error = 0 
    caseIds = checkComment(comment) 
    if not caseIds: 
        error = 1 
        tkMessageBox.showerror("Missing Case ID in check-in-comment", 
                               "Version:\n%s\n\nKommentar:\n%s" % 
                               (version, comment)) 
    sys.exit(error) 
 
# Remove # below to see what environment variables ClearCase sets. 
# 
#text = "\n".join( [" = ".join(x) for x in os.environ.items() 
#                   if x[0].startswith('CLEARCASE')]) 
#tkMessageBox.showinfo("Environment variable", text) 
     
if __name__ == '__main__':
    main()

####################################################################

# CommentPolicy2.py - Post Checkin Trigger 
import os, sys, re, tkMessageBox 
 
def checkComment(comment): 
    comment = comment.lower() 
    caseIds = re.findall(r'bug\d+|feat\d+',comment) 
    return caseIds 
 
def storeCheckInComment(caseIds, version, comment): 
    # In real life, this fuction would use ODBC, COM etc, not a dialog! 
    title = 'Store info in issue database' 
    message = ('Hello, can you store in the issue database\n'
               'that we got the following message:\n%s\n' 
               'when we checked in\n%s\n\n%s') % (" & ".join(caseIds), 
               version, comment) 
    if tkMessageBox.askyesno(title, message): 
        # Reply was yes
        return 0 
    else: 
        # Reply was no 
        return 1 
 
def main(): 
    comment = os.environ.get('CLEARCASE_COMMENT','') 
    version = os.environ['CLEARCASE_XPN'] 
 
    caseIds = checkComment(comment) 
    if not caseIds: 
        error = 1 
        tkMessageBox.showerror("Missing Case ID in check-in comment!!!", 
                               "Version:\n%s\n\nComment:\n%s" % 
                               (version, comment)) 
    else: 
        error = storeCheckInComment(caseIds, version, comment) 
        if error: 
            tkMessageBox.showerror("Error in issue database system!", 
                                   "Unable to store message:\n" 
                                   + comment) 
    sys.exit(error) 
 
if __name__ == '__main__':
    main()

####################################################################

# mktrig.py 
import os 
 
class Trigger: 
    def __init__(self, name, comment): 
        self.name = name 
        self.comment = comment 
 
    def run(self): 
        cmd = ('cleartool mktrtype %(type)s %(flags)s -c '
               '"%(comment)s" %(what)s %(name)s')
        args = {'type': self.type, 'flags': self.flags, 
                'comment' : self.comment, 
                'what': self.what, 'name': self.name} 
        print "Executing:" 
        print cmd % args 
        stdin, stdouterr = os.popen4(cmd % args) 
        stdin.close() 
        self.result = stdouterr.read() 
        stdouterr.close() 
 
class ElementTrigger(Trigger): 
    type = '-element' 
 
class TypeTrigger(Trigger): 
    type = '-type' 
 
class PreCITrigger(ElementTrigger): 
    flags = '-all -preop checkin' 
 
class PostCITrigger(ElementTrigger): 
    flags = '-all -postop checkin' 
 
class PythonExecMixIn: 
    def __init__(self, script): 
        self.what = '-exec "python %s"' % script 
 
class PythonPreCITrigger(PythonExecMixIn, PreCITrigger): 
    def __init__(self, name, comment, script): 
        Trigger.__init__(self, name, comment) 
        PythonExecMixIn.__init__(self, script) 
 
class PythonPostCITrigger(PythonExecMixIn, PostCITrigger): 
    def __init__(self, name, comment, script): 
        Trigger.__init__(self, name, comment) 
        PythonExecMixIn.__init__(self, script) 
 
trigger1 = PythonPreCITrigger('CommentPolicy', 
                    'Verify case id in check-in comment', 
                    '/path/to/CommentPolicy.py') 
trigger2 = PythonPostCITrigger('CommentPolicy2', 
                    'Report check-in to case handling system', 
                    '/path/to/CommentPolicy2.py') 
 
for trigger in [trigger1, trigger2]: 
    trigger.run() 
    print "Result:" 
    print trigger.result
