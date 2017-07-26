#  08-01-04
# v1.0.1
#


from copy import deepcopy

class ConfigObj:
    
    def __init__(self, indict, infile, stout):
        """This class creates a config object from a loaded config file - infile which should be passed in as a list of lines.
        It parses this file according to the config specification it is passed as infile - which specifies the keywords expected and the type of value expected.
        stout is an output object with a method stout.out('error line') for printing errors to.
        
        The value for each keyword in indict defines the type of value expected in the infile.
        Valid values are '' - a string value, '[]' multiple string values.
        
        Keyword and value can be escaped between ' ' or " " and be seperated by a space or = or : and other whitespace.
        A line can end with a trailing comment - which is marked by a # or a ;
        Lines of purely whitespace or only a comment will be ignored.

        The following are all valid entries :
        keyword1 value1         # trailing comment
        'keyword2' : 'value2'   ; and another trailing comment
        "keyword3" = [value3, 'value4',"value5"]

        The indict definition for the above config file would be a dictionary of the following construction :
        indict = { 'keyword1' : '', 'keyword2' :'', 'keyword3' : '[]' }
        There is a function called buildconfig in this distribution
        It builds a valid indict from a list of keywords - if a keyword ends in '[]' it makes it a multiple value.
        The valid construction then becomes :
        indict = buildconfig( ['keyword1', 'keyword2', 'keyword3[]'] ) 
    
        The parsed config is contained in object.config as a dictionary, keywords in indict that
        it failed to find valid entries for in infile will be set to None
        
        The config can be modified in place and then values written to a new file using the
        newfile = object.write() method or changed values written into an existing file using the
        newfile = object.update(infile) method.
        Both methods return the config files as a list of lines.
        
        A config file (infile) can have more parameters than the indict (extra ones will be ignored).
        This allows for multiple configs to be stored in a single file - keywords must be unique per file though.
        
        The created config dictionary object.config has the following values for each valid keyword :
        'value' and 'comment'. Comment is any trailing comment on the same line as the keyword.
        The comment is also written back by the write and update methods.
        
        If a keyword appears twice in a config file an error is written to stout - and the first value used.
        If an badly constructed or invalid line is found then an error is printed and the line ignored.
        
        If the value required is '[]' - multiple values - then the 'value' is returned as a list of strings.
        
        A single value cannot start with a '['.
        A value surrounded by '[ ]' will be assumed to be a multiple value entry. (even if there is none or only one value inside).

        The original parsed config is also preserved in object.defaultconfig so that the config produced can be amended and then reverted
        back to the original if desired (using a deepcopy operation).
        
        The indict (config spec) is also preserved as object.configspec
        This is so it can be used for writing out defaults by object.write() etc - when the original value is missing and
        ConfigObj has preserved a None.

        See the source code for the full specs for the write() method (which can take a writeorder
        paramater) and update(infile) method.
        There is also a useful getval(param) method which can be used as a handy shortcut for retrieving values.
        """

# make sure all the values are lowercase
        newdict = {}
        self.config = {}
        self.stout = stout # save the output object - this must be valid across the life of the config object
        for member in indict:
            newdict[member.lower()] = indict[member]
            self.config[member.lower()] = None       # values we fail to find later will be None.
        
        configkeys = newdict.keys()

        for line in infile:
            origline=line.strip()
            origparam = self.findparam(line)
            if not origparam:       # this line was whitespace or comment or invalid
                continue
            param=origparam.lower()
            if param not in newdict:    # a valid parameter - but not one we're looking for in this config object. Allows larger config files with multiple configs in - keywords must be unique per file though
                continue
            if param not in configkeys:
                stout.out('param defined twice : ')
                stout.out(origparam+'\n\n')
                continue
            #exception ? - parameter defined twice....... currently first parameter is used and second discarded.

            test = line.find(origparam)
            test += len(param)
            line = line[test+1:]
            value = self.findvalue(line)    # removes the dividing character between the parameter and value
            value, comment = self.removecomment(value, origline)
            if value == None:   # if the value was invalid
                continue
            value = self.matchvalue(value, newdict[param])  # this tests the value given is of the right type - and if a multipel value is required... returns it as a string.
            if value == None:      # is the value of the right type (single or multiple)
                stout.out('Wrong type, or invalid value in line : \n')
                stout.out(origline + '\n')
                stout.out('Expected value of type :\n')
                if newdict[param] == '[]':
                    paramtype = "['','',''] - Multiple Values"
                else:
                    paramtype = "'value' - Single Value" 
                stout.out(paramtype+'\n\n')
                continue                
            configkeys.remove(param)
            self.config[param] = {'value' : value, 'comment' : comment }
            
        self.defaultconfig = deepcopy(self.config)
        self.configspec = indict

    def findparam(self, line):
        """Extracts a valid parameter from a line in a config file -
        or returns None.
        A valid parameter is at the start of the line (excluding whitespace)
        and either between " " or ' ' or ends with a space.
        Invalid lines print an error and the line to stout using the
        stout.out(line) method."""
        line=line.strip()
        if line=='':                            # remove blank lines
            return None
        if line[0]== '#' or line[0]== ';':      # extract comments
            return None
        if line[0] =="'" or line[0] == '"':     #    if the keyword is escaped in quotes
            test = line[1:].find(line[0])
            if  test == -1: # if it starts with a quote but there isn't a second quote in the line
                self.stout.out("Badly formed line in config file (keyword doesn't have matching quotes): \n") 
                self.stout.out(line+'\n')
                return None
            else:
                param = line[1:test+1]
                return param

        test = line.find(' ')   # if we have no quotes we must have a space to seperate 
        if test == -1:          # if there are no quotes and no space then we have no keyword-value pair
            self.stout.out('Badly formed line in config file : \n') 
            self.stout.out(line+'\n\n')
            return None
        return line[:test]


    def findvalue(self, line):
        """Given a line with the keyword removed - the findvalue function returns the value
        and any trailing comment.
        It removes the dividing character and whitespace basically."""
        line=line.strip()
        if line[0] == ':' or line[0] == '=':
            line=line[1:]
            line=line.strip()
        return line

    def removecomment(self, line, origline):
        """Given a line containing a value (can be escaped by ' ' or " ") and possibly a comment
        It returns the tuple (value, comment). A comment will be preceded by # or ;.
        The comment value includes the # or ; if a comment is present - else ''.
        If a line is badly escaped an error is printed using the self.stout object."""
        line=line.strip()
        if line =='':
            self.stout.out("No value in line : \n") 
            self.stout.out(origline+'\n')
            return None
        if line[0] =="'" or line[0] == '"':     #    if the keyword is escaped in quotes
            test = line[1:].find(line[0])
            if  test == -1: # if it starts with a quote but there isn't a second quote in the line
                self.stout.out("Badly formed line in config file(value doesn't have matching quotes): \n") 
                self.stout.out(origline+'\n\n')
                return None, ''
            else:
                value = line[1:test+1]
                comment = line[test+2:].strip()
        else:
            test = line.find('#')
            if test == -1:
                test = line.find(';')
            if test == -1:      
                value = line
                comment = ''
            else:
                value = line[:test]            
                comment = line[test:].strip()
        if comment != '' and comment[0] != ';' and comment[0] != '#':
            self.stout.out("Badly formed line in config file (value or comment incorrectly formed): \n") 
            self.stout.out(origline.strip()+'\n\n')
            return None, ''
        return value, comment
    
    def matchvalue(self, value, param):
        """Given a value from a config file it checks that it is of the type sepcified in param.
        This will either be a string (param ='', value = anything !) or multiple strings
        (param = '[]', value=['any thing',"any thing",anything,.....]).
        It returns None (invalid value), a string, or a list of strings."""
        if value == '':
            if param == '[]':
                return None
            else:
                return ''
        if param == '[]':
            value=value.strip()
            if value[0] != '[' or value[-1] != ']':
                return None
            value = value[1:-1]
            newvals=[]
            value=value.lstrip()
            while len(value) > 0:                
                if value[0] == '\'' or value[0] == '"':
                    test = value[1:].find(value[0])
                    if  test == -1: # if it starts with a quote but there isn't a second quote in the line
#                        self.stout.out("Badly formed line in config file( a value doesn't have matching quotes): \n") 
#                        self.stout.out(origline+'\n')      # this error is also handled when matchvalue returns None
                        return None
                    else:
                        newvals.append(value[1:test+1])
                        value = value[test+2:].lstrip()
                        if value[0] == ',':
                            value = value[1:]
                            value=value.lstrip()
                else:
                    test=value.find(',')
                    if test != -1:
                        newvals.append(value[:test])
                        value = value[test+1:].lstrip()
                    else:
                        newvals.append(value)
                        value = ''
            return newvals
        if value[0] =='[':
            return None

        if value[0] == '\'' or value[0] == '"':
            test = value[1:].find(value[0])
            if  test == -1: # if it starts with a quote but there isn't a second quote in the line
                self.stout.out("Badly formed line in config file( a value doesn't have matching quotes): \n") 
                self.stout.out(origline+'\n')
                return None
            else:
                return value[1:test+1]
        else:
            return value.strip()
        
    def write(self, orderlist = None):
        """Takes the members of the config stored in this ConfigObj and returns them as a list.
        The order can be fixed using an iterator or sequence passed in.
        Comments in the config are preserved in the output list.
        If orderlist is present it will be iterated over and as valid keys for the config are
        found they will be used in that order.
        Extra values not in config but in orderlist are ignored.
        Any keywords in config but not in orderlist will be written out in whatever order they are produced from config !
        Any values in config that are of value None (weren't read in from the original file)
        *will* be output in the list - keywords specified in object.configspec as a single value type
        will be given the default value ''
        Multiple types will be given the default value []"""
        
        configkeys = self.config.keys()
        outorder = []
        if orderlist:
            for member in orderlist:
                outorder.append(member.lower())
        outconfig = []
        for member in outorder:
            if member in configkeys:
                configkeys.remove(member)
                if member.find("'") == -1:
                    outline = "'" + member + "'" + '    :    '
                elif member.find('"') == -1:
                    outline = '"' + member + '"' + '    :    '
                else:
                    outline = member + '    :    '
                if self.configspec[member] == '[]':
                    outline += '['
                    if not self.config[member]:
                        outline += ']'
                    else:
                        for item in self.config[member]['value']:
                            if item.find("'") == -1:
                                outline += "'" + item + "'" + ', '
                            elif item.find('"') == -1:
                                outline += '"' + item + '"' + ', '
                            else:
                                outline += item + ', '
                        outline = outline[:-1]
                        outline += ']'
                else:
                    if not self.config[member]:
                        outline += "''"
                    else:
                        if self.config[member]['value'].find("'") == -1:
                            outline += "'" + self.config[member]['value'] + "'"
                        elif self.config[member]['value'].find('"') == -1:
                            outline += '"' + self.config[member]['value'] + '"'
                        else:
                            outline += self.config[member]['value']
                if self.config[member]and self.config[member]['comment'] != '':
                    outline += '    ' + self.config[member]['comment']
                    
                outconfig.append(outline)
                
        for member in configkeys:
            if member.find("'") == -1:
                outline = "'" + member + "'" + '    :    '
            elif member.find('"') == -1:
                outline = '"' + member + '"' + '    :    '
            else:
                outline = member + '    :    '
            if self.configspec[member] == '[]':
                outline += '['
                if not self.config[member]:
                    outline += ']'
                else:
                    for item in self.config[member]['value']:
                        if item.find("'") == -1:
                            outline += "'" + item + "'" + ', '
                        elif item.find('"') == -1:
                            outline += '"' + item + '"' + ', '
                        else:
                            outline += item + ', '
                    outline = outline[:-1]
                    outline += ']'
            else:
                if not self.config[member]:
                    outline += "''"
                else:
                    if self.config[member]['value'].find("'") == -1:
                        outline += "'" + self.config[member]['value'] + "'"
                    elif self.config[member]['value'].find('"') == -1:
                        outline += '"' + self.config[member]['value'] + '"'
                    else:
                        outline += self.config[member]['value']
            if self.config[member]and self.config[member]['comment'] != '':
                outline += '    ' + self.config[member]['comment']
                
            outconfig.append(outline)
        return outconfig

    def update(self, infile):
        """Given a config file as a list of lines - infile - it updates any values it has in object.config
        It checks for lines that are valid parameters and in object.config and overwrites that line with it's stored value.
        Other lines are left untouched. Any keys not written by the ned of the file are tagged on the end.
        It doesn't terminate lines with a '\n' by the way :-)
        Nor does it report errors in infile - if you want to check infile you can create a new ConfigObj
        This just checks for valid known parameters and overwrites - ultra lightweight *ahem*....
        Useful though if you have a ConfigObj loaded from a file - the user has modified his settings
        and you want to write the new values out as a file.
        This method returns the new version of the file as a list of lines."""
	configkeys = self.config.keys()
	outconfig = []
        for line in infile:
            origline=line.strip()
            origparam = self.findparam(line)
            if not origparam:       # this line was whitespace or comment or invalid
                outconfig.append(line)
                continue
            member = origparam.lower()
            if member not in configkeys:    # a valid parameter - but not one we're looking for in this config object. Allows larger config files with multiple configs in - keywords must be unique per file though
                outconfig.append(line)
                continue
            else:
                configkeys.remove(member)
            if member.find("'") == -1:
                outline = "'" + member + "'" + '    :    '
            elif member.find('"') == -1:
                outline = '"' + member + '"' + '    :    '
            else:
                outline = member + '    :    '
            if self.configspec[member] == '[]':
                outline += '['
                if not self.config[member]:
                    outline += ']'
                else:
                    for item in self.config[member]['value']:
                        if item.find("'") == -1:
                            outline += "'" + item + "'" + ', '
                        elif item.find('"') == -1:
                            outline += '"' + item + '"' + ', '
                        else:
                            outline += item + ', '
                    outline = outline[:-1]
                    outline += ']'
            else:
                if not self.config[member]:
                    outline += "''"
                else:
                    if self.config[member]['value'].find("'") == -1:
                        outline += "'" + self.config[member]['value'] + "'"
                    elif self.config[member]['value'].find('"') == -1:
                        outline += '"' + self.config[member]['value'] + '"'
                    else:
                        outline += self.config[member]['value']
            if self.config[member]and self.config[member]['comment'] != '':
                outline += '    ' + self.config[member]['comment']
                
            outconfig.append(outline)

        for member in configkeys: # this gets any that have been missed out
            if member.find("'") == -1:
                outline = "'" + member + "'" + '    :    '
            elif member.find('"') == -1:
                outline = '"' + member + '"' + '    :    '
            else:
                outline = member + '    :    '
            if self.configspec[member] == '[]':
                outline += '['
                if not self.config[member]:
                    outline += ']'
                else:
                    for item in self.config[member]['value']:
                        if item.find("'") == -1:
                            outline += "'" + item + "'" + ', '
                        elif item.find('"') == -1:
                            outline += '"' + item + '"' + ', '
                        else:
                            outline += item + ', '
                    outline = outline[:-1]
                    outline += ']'
            else:
                if not self.config[member]:
                    outline += "''"
                else:
                    if self.config[member]['value'].find("'") == -1:
                        outline += "'" + self.config[member]['value'] + "'"
                    elif self.config[member]['value'].find('"') == -1:
                        outline += '"' + self.config[member]['value'] + '"'
                    else:
                        outline += self.config[member]['value']
            if self.config[member]and self.config[member]['comment'] != '':
                outline += '    ' + self.config[member]['comment']
                
            outconfig.append(outline)
        return outconfig
    
    def getval(self, param):
        """Return the value of the supplied param in object.config
        object.getval(param) is shorthand for object.config[param]['value']
        It can be further aliased in the following way :
        shortcut = object.getval
        shortcut(param) is then a shortcut(that looks like a function)
        which returns object.config[param]['value']"""
        if self.config[param] != None:
            return self.config[param]['value']
        else:
            return None


def buildconfig(params):
    """Given a list of the parameters of a config file - it will build the 
    dictionary used by ConfigObj to validate a config file.
    If the parameter passed to it ends in '[]' it will be made
    a list type."""
    outparams={} 
    for param in params:
        if param[-2:] !='[]':
            outparams[param]=''
        else:
            outparams[param[:-2]]="[]"
    return(outparams)
  
        
# Three simple example objects to use as the 'stout' object when forming a ConfigObj object
# For a better output object that logs to a file *and* prints to stdout
# see www.voidspace.org.uk/atlantibots/pythonutils.html

class test_out:
    """A very basic output object that just prints a line it is passed."""
    def out(self,line):
        print line,     # an even more basic version of this could have the command pass instead of print. It then becomes an object that ignores errors
        
class Stout_Errors:
    """A very basic output object that just saves lines it is passed in object.errors.
    It could be used to store the list of errors generated by a ConfigObj."""
    def __init__(self):
        self.errors = []
    def out(self, line):
        self.errors.append(line)

class Stout_Exceptions:
    """This traps some of the errors from a ConfigObj object.
    A more sensible thing to do would be to change the stout.out lines in CofigObj to raise exceptions.
    You can define which errors this traps by removing the 'elif' clauses selectively for errors you want to make non-fatal.
    You could also change the type of exception it raises to be more informative."""
    def out(self, line):
        if line== 'param defined twice :':
            raise Exception, 'Parameter defined twice in config file.'
        elif line == 'Wrong type, or invalid value in line : \n':
            raise Exception, 'Wrong type, or invalid value in line.'  # a multiple value where a single one was expected, or vice-versa - or a value is badly quoted etc.
        elif line == "Badly formed line in config file (keyword doesn't have matching quotes): \n": 
            raise Exception, "Badly formed line in config file (keyword doesn't have matching quotes)."
        elif line == 'Badly formed line in config file : \n':   # there is a keyword (without quotes) but no value effectively
            raise Exception, "Badly formed line in config file - probably a missing value."
        elif line == "No value in line : \n":   # there is a keyword but no value
            raise Exception, "Missing value in a line in the config file."
        elif line == "Badly formed line in config file (value or comment incorrectly formed): \n":   # missing quotes
            raise Exception, "Badly formed line in config file - probably a missing quote."
        else:
            print line,


if __name__ == '__main__':

            
    stout = test_out()
# If you wanted to trap errors instead of printing them use :
# stout = Stout_Errors()
# after parsing stout.errors holds a list of all the errors.
# Alternatively for a silly example of a stout object that traps errors and raises an exception instead.
# stout = Stout_Exceptions()
# For a better output object that logs to a file *and* prints to stdout 
# see StandOut at www.voidspace.org.uk/atlantibots/pythonutils.html

    testfile = ['# hello test comment \n','\n','   \n','hello goodbye\n',"'hello2' 'goodbye2' # trailing comment\n",
                '; atlantis style comment\n','"hello3"  :   "goodbye3"\n','"hello4" : [goodbye4,goodbye5,goodbye6] ; another trailing comment\n']
    testdict = { 'hello' : '', 'hello2' : '', 'hello3' : '', 'hello4' :'[]', 'hello5' : ''}
    config = ConfigObj(testdict, testfile, stout)
    print "Having created a ConfigObj from a test dictionary let's see how it parsed the test dictionary  (one of the values is deliberately missing) :"
    print
    for member in config.config:
        print member, ' : ', config.config[member]

    print
    print
    print "Next we'll ask it to write back out the config and tell it what order to do it in, see the missing value is output with a default one : "
    print
    configout = config.write(['hello','hello2','hello3','another value','hello4'])
    for line in configout:
        print line
    print
    print
    print "Next we'll reverse the order of the config file and get it to 'update' this  - again see the missing value at the end :"
    testfile.reverse()
    configout = config.update(testfile)
    for line in configout:
        print line
    print
    print
# Now for some error testing :-)

    print "Using the same test dictionary we'll give it a badly built file and see the errors it throws up :"
    print
    testfile = ['# Another test comment \n','\n','   \n',"""hellogoodbye\n""","""'hello2' "goodbye2' # trailing comment""",
                '; atlantis style comment\n','"hello3"  :   [test]\n','"hello4" : ["goodbye4,goodbye5,goodbye6] ; another trailing comment\n']
    
    config2 = ConfigObj(testdict, testfile, stout)
    print "See what ends up in the ConfigObj :"
    print
    for member in config2.config:
        print member, ' : ', config2.config[member]
    dummy = raw_input('Wait for Enter before vanishing.....')
