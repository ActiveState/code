import sys

#this class gets all output directed to stdout(e.g by print statements)
#and stderr and redirects it to a user defined function
class PrintHook:
    #out = 1 means stdout will be hooked
    #out = 0 means stderr will be hooked
    def __init__(self,out=1):
        self.func = None##self.func is userdefined function
        self.origOut = None
        self.out = out

    #user defined hook must return three variables
    #proceed,lineNoMode,newText
    def TestHook(self,text):
        f = open('hook_log.txt','a')
        f.write(text)
        f.close()
        return 0,0,text

    def Start(self,func=None):
        if self.out:
            sys.stdout = self
            self.origOut = sys.__stdout__
        else:
            sys.stderr= self
            self.origOut = sys.__stderr__
            
        if func:
            self.func = func
        else:
            self.func = self.TestHook

    #Stop will stop routing of print statements thru this class
    def Stop(self):
        self.origOut.flush()
        if self.out:
            sys.stdout = sys.__stdout__
        else:
            sys.stderr = sys.__stderr__
        self.func = None

    #override write of stdout        
    def write(self,text):
        proceed = 1
        lineNo = 0
        addText = ''
        if self.func != None:
            proceed,lineNo,newText = self.func(text)
        if proceed:
            if text.split() == []:
                self.origOut.write(text)
            else:
                #if goint to stdout then only add line no file etc
                #for stderr it is already there
                if self.out:
                    if lineNo:
                        try:
                            raise "Dummy"
                        except:
                            newText =  'line('+str(sys.exc_info()[2].tb_frame.f_back.f_lineno)+'):'+newText
                            codeObject = sys.exc_info()[2].tb_frame.f_back.f_code
                            fileName = codeObject.co_filename
                            funcName = codeObject.co_name
                    self.origOut.write('file '+fileName+','+'func '+funcName+':')                    
                self.origOut.write(newText)
                

    #pass all other methods to __stdout__ so that we don't have to override them
    def __getattr__(self, name):
        return self.origOut.__getattr__(name)
    
if __name__ == '__main__':
    
    def MyHookOut(text):
        return 1,1,'Out Hooked:'+text
    
    def MyHookErr(text):
        f = open('hook_log.txt','a')
        f.write(text)
        f.close()
        return 1,1,'Err Hooked:'+text
    
    print 'Hook Start'
    phOut = PrintHook()
    phOut.Start(MyHookOut)
    phErr = PrintHook(0)
    phErr.Start(MyHookErr)
    print 'Is this working?'
    print 'It seems so!'
    phOut.Stop()
    print 'STDOUT Hook end'
    compile(',','<string>','exec')
    phErr.Stop()
    print 'Hook end'
        
