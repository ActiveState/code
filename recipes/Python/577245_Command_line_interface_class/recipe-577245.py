    #Covered by GPL V2.0


    import sys
    try:
        import readline 
    except:
        pass

    class Console:
        def __init__(self,prompt):
            self.prompt=prompt
            self.banner=""
    
            self.commands={}
            self.commandSort=[]
    
    
            for i in dir(self):
                if "CMD_"==i[:4]:
                    cmd=i.split("CMD_")[1].lower()
                    self.commands[cmd]=getattr(self,i)
                    try:
                        self.commandSort.append((int(self.commands[cmd].__doc__.split("|")[0]),cmd))
                    except:
                        print ("Docstring for command must have the following format: '(number)|(string)[|(string)]+' # Two or more strings")
            
            self.commandSort.sort()
            self.commandSort=[i[1] for i in self.commandSort]
    
            #######   DEFAULT VARS (begins with CFG_)  ###########################
            self.CFG_DEBUG=False
    
            self.configvars={}
            for i in dir(self):
                if "CFG_"==i[:4]:
                    var=i.split("CFG_")[1]
                    self.configvars[var]=i
    
        def setBanner(self,banner):
            self.banner=banner
    
        def run(self):
            print self.banner
            while True:
                try:
                    command=raw_input(self.prompt)
                    self.execCommand(command)
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                except Exception,a:
                    self.printError (a)
    
            print ("\r\n\r\nBye!...")
            sys.exit(0)
    
    
        def printError(self,err):
            sys.stderr.write("-- Error: %s\r\n" % (str(err),))
            if self.CFG_DEBUG:
                pass
    
        def execCommand(self,cmd):
            words=cmd.split(" ")
            words=[i for i in words if i]
            if not words:
                return
            cmd,parameters=words[0].lower(),words[1:]
    
            if not cmd in self.commands:
                raise Exception("Command '"+cmd+"' not found. Try 'help'\r\n")
    
            self.commands[cmd](*parameters)
    
        ######## DEFAULT COMMANDS (begins with CMD_) ################
    
        def CMD_help(self,*args):
            '''-3|help|Show's help'''
            print (self.banner)
    
    
            alldata=[]
            lengths=[]
    
            for i in self.commandSort:
                alldata.append(self.commands[i].__doc__.split("|")[1:])
    
            for i in alldata:
                if len(i) > len(lengths):
                    for j in range(len(i)-len(lengths)):
                        lengths.append(0)
    
                j=0
                while j<len(i):
                    if len(i[j])>lengths[j]:
                        lengths[j]=len(i[j])
                    j+=1
    
            print ("Help")
            print ("-"* (lengths[0]+lengths[1]+4))
            print 
    
            for i in alldata:
                print (("%-"+str(lengths[0])+"s  - %-"+str(lengths[1])+"s") % (i[0],i[1]))#lengths))
                if len(i)>2:
                    for j in i[2:]:
                        print (("%"+str(lengths[0]+9)+"s* %s") % (" ",j))
                    print 
            print
    
    
        def CMD_config(self,*args):
            '''-2|config|Show config variables'''
            print ("Configuration variables\r\n"+"-"*79)
            for i,j in self.configvars.items():
                value=self.parfmt(repr(getattr(self,j)),52)
                print ("| %20s | %52s |" % (i,value[0]))
                for k in value[1:]:
                    print ("| %20s | %52s |" % ("",k))
                if len(value)>1:
                    print("| %20s | %52s |" % ("",""))
    
            print ("-"*79)
    
            print 
    
        def parfmt(self,txt,width):
            res=[]
            pos=0
            while True:
                a=txt[pos:pos+width]
                if not a:
                    break
                res.append(a)
                pos+=width
    
            return res
            
    
        def CMD_set(self,*args):
            '''-1|set [variable_name] [value]|Set configuration variable value|Values are python expressions: 1, True, "How are you".lower()'''
            value=" ".join(args[1:])
    
            if args[0] not in self.configvars:
                raise Exception("Variable %s doesn't exist" % (args[0]))
    
            setattr(self,"CFG_"+args[0],eval(value))


    ################# CALCULATOR EXAMPLE ######################


    class calculator(Console):
        def __init__(self):
            self.CFG_var1=28                     # Config variable before call superclass constructor
            Console.__init__(self,prompt="Calculator Cli: ") # Specify the prompt

        def CMD_sum(self,*args):
            '''5|sum val1 val2|Makes the sum of val1 and val2'''  # Docstring format: Preference order in help | command syntax | help string
            print int(args[0])+int(args[1])
 
        def CMD_sub(self,*args):
            '''6|sub val1 val2|Makes the substraction of val1 and val2'''
            print int(args[0])-int(args[1])

 
    a=calculator()
    a.run()

    ############################# DEMO ##############################################

    $ python example.py

    Calculator Cli: help

    Help
    ----------------------------------------------------------------------

    help                         - Show's help                        
    config                       - Show config variables              
    set [variable_name] [value]  - Set configuration variable value   
                                        * Values are python expressions: 1, True, "How are you".lower()

    sum val1 val2                - Makes the sum of val1 and val2     
    sub val1 val2                - Makes the substraction of val1 and val2

    Calculator Cli: sum 4 9
    13
    Calculator Cli: sub 5 8
    -3
    Calculator Cli: config
    Configuration variables
    -------------------------------------------------------------------------------
    |                DEBUG |                                                False |
    |                 var1 |                                                   28 |
    -------------------------------------------------------------------------------

    Calculator Cli: set var1 59
    Calculator Cli: config
    Configuration variables
    -------------------------------------------------------------------------------
    |                DEBUG |                                                False |
    |                 var1 |                                                   59 |
    -------------------------------------------------------------------------------

    Calculator Cli:
