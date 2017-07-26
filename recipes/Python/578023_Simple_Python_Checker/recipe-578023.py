"""
    @author    Thomas Lehmann
    @file      simple-python-checker.py
    @language  pypy 1.7 and python 3.2 have been used

    @note Using the tool against itself should never throw any warning or error!
    @note I don't use TAB's and indentation is 4.
    @note I'm using the documentation tool 'epydoc' (http://epydoc.sourceforge.net/)
          for generating HTML documentation of this.

    @todo verifying that given file is a python file
    @todo allow first parameter for tool to be a folder/path instead of a file.
    @todo new limit: relation of code/comments per file
    @todo new limit: relation of code/comments per class
    @todo new limit: relation of code/comments per function/method

    @see <a href="http://en.wikipedia.org/wiki/Source_lines_of_code">
          http://en.wikipedia.org/wiki/Source_lines_of_code</a>
    @see <a href="http://www.dwheeler.com/sloccount/sloccount.html">
          http://www.dwheeler.com/sloccount/sloccount.html</a>
"""
__docformat__ = "javadoc en"

import sys
import os
import ast

class GreenYellowRedLimit:
    """ this class handles three ranges: green, yellow and red.
        <ul>
            <li><b>green</b>:  indicates that a value is valid
            <li><b>yellow</b>: indicates that the value is accepted but not ok.
                               A warning message will be generated.
            <li><b>red</b>:    indicates an unacceptable state.
                               An error message will be generated.
        </ul>
    """
    def __init__(self, maxGreen, maxYellow, message):
        """ stores limit information
            @param maxGreen
                        is the maximum value which is valid
            @param maxYellow
                        is the maximum value for warning. Is the value more
                        then it is an error.
            @param message
                        is the message printed when the limit is at least
                        more than maxGreen.
        """
        self.maxGreen  = maxGreen
        self.maxYellow = maxYellow
        self.message   = message

    def isGreenFor(self, value):
        """ Checking for a value to be in a valid range.
            @param  value
                        that value to check to be in green state (valid)
            @return true when the given value is valid.
        """
        return value <= self.maxGreen

    def isRedFor(self, value):
        """ Checking for a value to be in an invalid range.
            @param  value
                        that value to check to be in red state (invalid)
            @return true when the given value is invalid.
        """
        return value > self.maxYellow

    def getMessage(self, pathAndFileName, lineNr, value):
        """ generates printable warning/error message
            @param pathAndFileName
                    path and filename of the pyton file
            @param lineNr
                    that line the warning/error refers to
            @param value
                    that value that raises the warning/error

            @note It is assumed that the "not green" status has
                  been checked before.
        """
        prompt = "%s" % pathAndFileName

        if lineNr >= 0: prompt += "(%d): " % lineNr
        else:           prompt += "(1): "

        if value > self.maxYellow: prompt += "error: "
        else:                      prompt += "warning: "

        return prompt + self.message + ", value is %d" % value + \
               " (green<=%d,yellow>=%d,red>=%d)" % \
               (self.maxGreen, self.maxGreen+1, self.maxYellow+1)

class Limits:
    """ Does group all limits to be checked by this scripts """
    def __init__(self):
        """ initializes container for limit defintions only """
        self.definitions = {}

    def registerLimit(self, name, limit):
        """ registration of a limit
            @param name
                    name of the limit
            @param limit
                    instance of GreenYellowRedLimit class
        """
        if not name in self.definitions:
            self.definitions[name] = limit
        return limit

    def maxAttributesPerClass(self):
        """ <b>Too many attributes per class</b>:<br>
            Is an indicator for bad design. Maybe the class is too complex or an
            improper way to store information has been used. """
        return self.registerLimit(self.maxAttributesPerClass.__name__, \
            GreenYellowRedLimit( 10,  15, "too many attributes in class"))

    def maxFunctionsPerClass(self):
        """ <b>Too many functions per class</b>:<br>
            Is an indicator for bad design. Maybe the class does handle too much. """
        return self.registerLimit(self.maxFunctionsPerClass.__name__, \
            GreenYellowRedLimit( 15,  20, "too many functions in class"))

    def maxFunctionsPerFile(self):
        """ <b>Too many functions per file</b>:<br>
            Is an indicator for bad design. You have too many logic in one file.
            The different to many functions per class is that global functions are
            counted as well as functions of multiple classes in same file. """
        return self.registerLimit(self.maxFunctionsPerFile.__name__, \
            GreenYellowRedLimit( 35,  40, "too many functions in file"))

    def maxClassesPerFile(self):
        """ <b>Too many classes per file</b>:<br>
            Is an indicator for bad design and/or simply the fact that the file
            could be splitted up for different classes. """
        return self.registerLimit(self.maxClassesPerFile.__name__, \
            GreenYellowRedLimit(  4,   6, "too many classes in file"))

    def maxParametersPerFunction(self):
        """ <b>Too many parameters in function/method</b>:<br>
            Is an indicator for bad design. Are many of those parameters also required
            by other functions or methods? Can't you provide a class or a dictionary? """
        return self.registerLimit(self.maxParametersPerFunction.__name__, \
            GreenYellowRedLimit(  3,   5, "too many parameters in function/method"))

    def maxLinesPerFunction(self):
        """ <b>Too many lines per function/method</b>:<br>
            The idea is to have - more or less - the content of the whole function
            or method visible on one screen to avoid scrolling. On Windows I have
            a "Courier New" font with size 10 and that's really not too big and not too
            small; with this I can see about 50 lines of code. With an output window or
            other information at the bottom (IDE) you will see less than this. This metric
            includes comments, excludes blanks."""
        return self.registerLimit(self.maxLinesPerFunction.__name__, \
            GreenYellowRedLimit( 50, 100, "too many lines in function/method"))

    def maxControlStatementsPerFunction(self):
        """ <b>Too many control statements</b>:<br>
            Is an indicator that the function/method is too complex. """
        return self.registerLimit(self.maxControlStatementsPerFunction.__name__, \
            GreenYellowRedLimit( 15,  20, "too many control statements"))

    def maxCharactersPerLine(self):
        """ <b>Line too long</b>:<br>
            I want to see the whole line without scrolling. Another aspect of this
            is when you use tools for comparing two versions (side by side) or
            when printing it out; it's to avoid wrapping code into the next lines.
            <b>It's about readability!</b> """
        return self.registerLimit(self.maxCharactersPerLine.__name__, \
            GreenYellowRedLimit( 95, 110, "line too long"))

    def maxLinesPerFile(self):
        """ <b>Too many lines in file</b>:<br>
            Is an indicator for bad design. I know from files with several thousand
            lines of code and especially those file mostly are difficult to maintain.
            This metric includes comments, excludes blank lines. """
        return self.registerLimit(self.maxLinesPerFile.__name__, \
            GreenYellowRedLimit(550, 750, "too many lines in file"))

    def maxIndentationLevel(self):
        """ <b>Too many indentation levels</b>:<br>
            Is an indicator that the code is too complex! It's about examples like having
            an if statement containing an if statement and again containing an if
            statement and again ... """
        return self.registerLimit(self.maxIndentationLevel.__name__, \
            GreenYellowRedLimit(  3,   5, "too many indentation levels"))

    def maxTabs(self):
        """ <b>Too many tabs</b>:<br>
            This a visual style issue. You can disallow tabs if wanted.
            Default: no tabs are allowed. """
        return self.registerLimit(self.maxTabs.__name__, \
            GreenYellowRedLimit(  0,   0, "too many tabs"))

FILE     = 0
CLASS    = 1
FUNCTION = 2
LINENR   = 3
LEVEL    = 4

class FileData:
    """ represent all information for one file from one analyse """
    def __init__(self, pathAndFileName):
        """ initializes members for one file analyse """
        self.pathAndFileName = pathAndFileName
        self.classes         = {}
        self.attributes      = {}
        self.functions       = {}

        self.errors          = 0
        self.warnings        = 0
        self.totalLines      = 0
        self.totalBlankLines = 0
        self.messages        = []

class SimplePythonChecker(ast.NodeVisitor):
    """ As visitor on one side it can traverse the python code
        for checking structural things. Comments, length of lines,
        indentation depth are topic which need to be handled separately.

        @note The tool does not check whether somebody creates attributes
              outside of the __init__ method.
    """
    def __init__(self):
        """ initializing to have some empty containers and the limits """
        self.limits     = Limits()
        self.current    = {LEVEL: 0}
        self.files      = {}

    def analyze(self, pathAndFileName):
        """ main method for analyzing one python file
            @param pathAndFileName
                    path and filename of a python file to analyze"""
        print("...analyzing %s..." % pathAndFileName)
        # remember the current file for further processing
        newFileData = FileData(pathAndFileName)
        self.files[pathAndFileName] = newFileData
        self.current[FILE]          = newFileData

        # the content of the whole file
        code = open(pathAndFileName).read()
        # collecting relevant information for limit checking walking the AST tree.
        tree = ast.parse(code)
        self.visit(tree)
        # line based analyse
        self.analyzeCode(code)
        # checking collected information
        self.checkLimits()
        self.finalize()

    def analyzeCode(self, code):
        """ line based analyse.
            @param code
                    the content of the whole file (usually) """
        currentFile = self.current[FILE]

        # checking all line lengths for given file (code)
        lineNr       = 1
        for line in code.split('\n'):
            # checking for line length
            limitToCheck = self.limits.maxCharactersPerLine()
            value        = len(line)
            self.checkLimit(lineNr, limitToCheck, value)

            # checking for tabs in line
            limitToCheck = self.limits.maxTabs()
            value        = line.count("\t")
            self.checkLimit(lineNr, limitToCheck, value)

            # counting blank lines
            if len(line.strip()) == 0:
                currentFile.totalBlankLines += 1
                functions = [ function for function in currentFile.functions.values() \
                              if function["lineNr"]                   < lineNr and \
                                 function["lineNr"]+function["lines"] > lineNr ]

                if len(functions) == 1:
                    functions[0]["blankLines"] += 1

            lineNr += 1

        # checking number of lines in given file (code)
        limitToCheck = self.limits.maxLinesPerFile()
        lineNr       = 1
        value        = code.count("\n") + 1
        self.checkLimit(lineNr, limitToCheck, value - currentFile.totalBlankLines)

        currentFile.totalLines = value

    def visit_ClassDef(self, node):
        """ stores the class.
            @param node
                    walking the AST tree a class definition has been found
        """
        currentFile = self.current[FILE]

        newClass               = {}
        newClass["lineNr"]     = node.lineno
        newClass["attributes"] = set()
        newClass["functions"]  = set()

        currentFile.classes[node.name] = newClass
        self.current[CLASS] = node.name
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """ stores attributes and counts them class wise
            @param node
                walking the AST tree an attribute has been found. In python you
                cannot declare so I decide that the c'tor (__init__) has to initialize
                all valid members and only those count for the limit checking
        """
        currentFile = self.current[FILE]

        if FUNCTION in self.current and self.current[FUNCTION] == "__init__":
            newAttribute           = {}
            newAttribute["lineNr"] = node.lineno

            # provide class information (when available)
            if CLASS in self.current and self.current[CLASS]:
                newAttribute["class"] = self.current[CLASS]
                currentFile.classes[self.current[CLASS]]["attributes"].add(node.attr)

            currentFile.attributes[node.attr] = newAttribute
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """ stores function and register it at class if it's a method.
            @param node
                walking the AST tree a function/method definition has been found.
                It's to check for too many parameters, for too many lines in
                a function/method and for complexity.
        """
        currentFile = self.current[FILE]

        newFunction               = {}
        newFunction["lineNr"]     = node.lineno
        newFunction["cstms"]      = 0
        newFunction["blankLines"] = 0

        # this is because of handling different python versions...
        try:    newFunction["argumentNames"] = [arg.arg for arg in node.args.args]
        except: newFunction["argumentNames"] = [arg.id for arg in node.args.args]

        # provide class information (when available)
        if CLASS in self.current and self.current[CLASS]:
            currentClass = currentFile.classes[self.current[CLASS]]
            if node.lineno <= currentClass["lineNr"]:
                self.current[CLASS] = None
            else:
                newFunction["class"] = self.current[CLASS]
                currentClass["functions"].add(node.name)

        currentFile.functions[node.name] = newFunction
        self.current[FUNCTION] = node.name
        self.generic_visit(node)
        # calcuates number of lines of function/method
        newFunction["lines"] = self.current[LINENR] - node.lineno
        self.current[FUNCTION]  = None

    def visit_If(self, node):
        """ required to check for indentation level and complexity """
        currentFile = self.current[FILE]
        self.current[LEVEL] += 1

        limitToCheck = self.limits.maxIndentationLevel()
        lineNr       = node.lineno
        value        = self.current[LEVEL]

        self.checkLimit(lineNr, limitToCheck, value)

        if self.current[FUNCTION] in currentFile.functions:
            currentFunction = currentFile.functions[self.current[FUNCTION]]
            currentFunction["cstms"] += 1

        self.generic_visit(node)
        self.current[LEVEL] -= 1

    def visit_For(self, node):
        """ required to check for indentation level and complexity
            @param node
                This node represents an 'if' statement (if, elif and else)
        """
        currentFile = self.current[FILE]
        self.current[LEVEL] += 1

        limitToCheck = self.limits.maxIndentationLevel()
        lineNr       = node.lineno
        value        = self.current[LEVEL]

        self.checkLimit(lineNr, limitToCheck, value)

        if self.current[FUNCTION] in currentFile.functions:
            currentFunction = currentFile.functions[self.current[FUNCTION]]
            currentFunction["cstms"] += 1

        self.generic_visit(node)
        self.current[LEVEL] -= 1

    def visit_While(self, node):
        """ required to check for indentation level and complexity """
        currentFile = self.current[FILE]

        self.current[LEVEL] += 1

        limitToCheck = self.limits.maxIndentationLevel()
        lineNr       = node.lineno
        value        = self.current[LEVEL]

        self.checkLimit(lineNr, limitToCheck, value)

        if self.current[FUNCTION] in currentFile.functions:
            currentFunction = currentFile.functions[self.current[FUNCTION]]
            currentFunction["cstms"] += 1

        self.generic_visit(node)
        self.current[LEVEL] -= 1

    def visit_Return(self, node):
        """ required to check for complexity """
        currentFile = self.current[FILE]

        if self.current[FUNCTION] in currentFile.functions:
            currentFunction = currentFile.functions[self.current[FUNCTION]]
            currentFunction["cstms"] += 1

        self.generic_visit(node)

    def checkLimits(self):
        """ checking different limits """
        currentFile = self.current[FILE]

        for className in currentFile.classes:
            # checking for number of attributes/members per class
            limitToCheck = self.limits.maxAttributesPerClass()
            value        = len(currentFile.classes[className]["attributes"])
            lineNr       = currentFile.classes[className]["lineNr"]
            self.checkLimit(lineNr, limitToCheck, value)

            # checking for number of functions/methods per class
            limitToCheck = self.limits.maxFunctionsPerClass()
            value        = len(currentFile.classes[className]["functions"])
            self.checkLimit(lineNr, limitToCheck, value)

        for functionName in currentFile.functions:
            # checking for number of parameters per function/method
            limitToCheck = self.limits.maxParametersPerFunction()
            lineNr       = currentFile.functions[functionName]["lineNr"]
            value        = len(currentFile.functions[functionName]["argumentNames"])

            if "self" in currentFile.functions[functionName]["argumentNames"]:
                value -= 1

            self.checkLimit(lineNr, limitToCheck, value)

            # checking for number of lines per function/method
            limitToCheck = self.limits.maxLinesPerFunction()
            value        = currentFile.functions[functionName]["lines"]
            value       -= currentFile.functions[functionName]["blankLines"]
            self.checkLimit(lineNr, limitToCheck, value)
            # checking for number of control statements per function/method
            limitToCheck = self.limits.maxControlStatementsPerFunction()
            value        = currentFile.functions[functionName]["cstms"]
            self.checkLimit(lineNr, limitToCheck, value)


        # checking number of functions/methods per file
        limitToCheck = self.limits.maxFunctionsPerFile()
        value        = len(currentFile.functions)
        lineNr       = 1
        self.checkLimit(lineNr, limitToCheck, value)
        # checking number of classes per file
        limitToCheck = self.limits.maxClassesPerFile()
        value        = len(currentFile.classes)
        self.checkLimit(lineNr, limitToCheck, value)

    def checkLimit(self, lineNr, limitToCheck, value):
        """ checks for a single limit and prints a message
            if given value is not valid """
        currentFile = self.current[FILE]

        if not limitToCheck.isGreenFor(value):
            message = limitToCheck.getMessage(currentFile.pathAndFileName, lineNr, value)
            currentFile.messages.append((lineNr, message))
            if limitToCheck.isRedFor(value): currentFile.errors   += 1
            else:                            currentFile.warnings += 1

    def generic_visit(self, node):
        """ main reason for overwriting this method is to be able to
            calculate how many line are in a block (function/method/class/...) """
        try:    self.current[LINENR] = node.lineno
        except: pass
        # traverse further nodes
        ast.NodeVisitor.generic_visit(self, node)

    def finalize(self):
        """ printing some final information from last analyse """
        currentFile = self.current[FILE]

        for message in sorted(currentFile.messages):
            print(message[1])

        functions = [name for name in currentFile.functions \
                     if len(currentFile.functions[name]["argumentNames"]) == 0 or \
                        not currentFile.functions[name]["argumentNames"][0] == 'self']

        print("...%3d lines processed (with %d blank lines)" \
              % (currentFile.totalLines, currentFile.totalBlankLines))
        print("...%3d function(s) processed" % len(functions))
        print("...%3d method(s) processed" % (len(currentFile.functions) - len(functions)))
        print("...%3d warning(s) - %d error(s)" \
              % (currentFile.warnings, currentFile.errors))

def main():
    """ script can be executed with filename as parameter, otherwise the
        script itself will be checked """
    print("Simple Python Checker v0.2 by Thomas Lehmann")
    print("...running Python %s" % sys.version.replace("\n", " - "))
    checker = SimplePythonChecker()
    if len(sys.argv) == 2:
        pathAndFileName = sys.argv[1].strip()
        if os.path.isfile(pathAndFileName):
            checker.analyze(pathAndFileName)
        else:
            print("...error: file '%s' does not exist" % pathAndFileName)
    else:
        checker.analyze("simple-python-checker.py")

if __name__ == "__main__":
    main()
