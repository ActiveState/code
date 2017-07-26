'''
Yaptoo (Yaptu Outrageously Obfuscated) by Michael Palmer
based on: Yaptu (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52305) by Alex Martelli

Changes from Yaptu:
- separated template compilation from merging
- added some error reporting
- changed default template syntax (It remains easy to make your own by defining a bunch of regexes)
- added syntax for comments
- added Cheetah-style variable substitution
- limited flow control to 'for' and 'if'
- added 'include' function

Limitations:
- Statements, expressions, or comments cannot span multiple lines
- In 'for' loops, there is neither 'break' nor 'continue'
- No 'controller' behaviour of any kind, i.e. you cannot run templates in a 'standalone' fashion.

Yaptoo is intended solely for use in an auxiliary role.
It is lightweight and fast.
'''

import re, os.path
from cStringIO import StringIO

try:
    from traceback import format_exc
except: # lacking before 2.4
    def format_exc():
        s = cStringIO.StringIO()
        traceback.print_exc(file=s)
        return s.getvalue()


class YaptooError(Exception):
    pass


class YaptooErrorHandler(object):
    '''
    used per inheritance by both Template and _Merger classes
    '''
    verboseErrors = False

    def error(self, offense, comment=None):
        '''
        wrap Exception so that user better sees what happened where.
        '''

        packagedInfo=['\n---------------------']
        if comment:
            packagedInfo.append(comment)
        packagedInfo.append("Offensive statement or expression: %s" % offense)
        packagedInfo.append('Underlying exception:')
        packagedInfo.append(format_exc().splitlines()[-1])

        # annotate with the proper source line
        stmt, src, num = self.lines[self.currentLine]
        packagedInfo.append("\nSource line: %s \nLine number: %d\nSource file: %s" % (stmt.strip(), num+1, src) )

        if self.verboseErrors and hasattr(self, 'globals'):
            packagedInfo.append('Variables available when exception occured:')

            globs = self.globals.copy()
            # remove confusing things from the namespace...
            globs.pop('__builtins__', None)
            globs.pop('_mergeBlock__', None)
            globs.pop('_resolveSimple__', None)

            items = globs.items()
            items.sort()

            def printNice(item, indent=20):
                from pprint import pformat
                out = []
                fill = ' ' * indent

                k,v = item
                dataList = pformat(v).split('\n')
                out=[]
                out.append(k.ljust(indent) + dataList.pop(0))
                for l in dataList:
                    out.append(fill + l)
                return '\n'.join(out)

            for it in items:
                packagedInfo.append('' + printNice(it))

        packagedInfo.append('---------------------')

        raise YaptooError, '\n'.join(packagedInfo)


class Template(YaptooErrorHandler):
    '''
    Base class for compiling template definition files or strings
    '''
    ## Begin template syntax definition

    # 'expressionRegex': this regex is used to identify Python expressions
    # I like this style, it stands out well in HTML
    # however, you need to avoid  ']]' in python expressions such as lists of lists,
    # e.g. by inserting a space:  [[a,b], [c,d] ]
    # alternatively you could use
    # re.compile("\<\<\s*(.*?)\s*\>\>"),                    # example: << i**33 >>
    #  - safe, but does not stand out well in html
    expressionRegex = re.compile("\[\[\s*(.*?)\s*\]\]")     # example: [[ i**33 ]]

    # this regex identifies comments (comments will be stripped from the output)
    commentRegex = re.compile('\s*##.*')                    # like so: this will print ## but this won't

    # include directives
    includeRegex = re.compile(r'\s*#include\s+([\/\\]?\w+(\.\w+)*([\/\\]\w+(\.\w+)*)*)')

    # this regex is for flow control statements. It must capture the statement itself but nothing else.
    # here, statements are prefixed with #:  #for x in y:   #end for, #if, #else:  , #end if
    statementRegex = re.compile(r'\s*#(for .+?:|if .+?:|elif .+?:|else:|end (?:if|for))\s*')

    # these two regexes are solely for catching a specific unworkable syntax in for-in statements
    forInDottedRe = re.compile('for\s.*?\$[^\,]*?\..*?\sin')  #
    # the regex below depends on the one above
    forInRe = re.compile('(for\s.*?\sin)(.+)', re.DOTALL)

    # a regex that will catch other Miss Happen-Statements. Note that on any line it will be tried
    # only after statementRegex, so it doesn't hurt if the regex by itself would also match valid statements
    faultyStatement = re.compile(r'\s*#.*')            # will capture anything like '#howdi, rowdy!',

    # this marker at the end of a line will consume the linebreak and all subsequent continuous whitespace
    joinLines = re.compile('\:\>\s+', re.DOTALL)            # :>

    # good ol $varname substitution
    simpleSubstitutionRegex = re.compile("\$((?:[a-zA-Z_]\w*)(?:\.\$?[a-zA-Z_]\w*)*)")

    ## End template syntax definition

    def __init__( self,
                  sourceString=None,
                  sourceFile=None,
                  templateDir='',
                  stripEmptyLines = False,
                  renderMissingNames = False,
                  renderMissingFormat = '<span style="color:red">%s</span>'
                ):

        self.templateDir = templateDir
        self.stripEmptyLines = stripEmptyLines
        self.renderMissingNames = renderMissingNames
        self.renderMissingFormat = renderMissingFormat

        assert(sourceString and not sourceFile) or (sourceFile and not sourceString), 'Must pass either file or string, not both'

        # compile the template
        source = sourceString or sourceFile

        # figure out whether we have a string or a file
        if sourceFile:
            if not hasattr(sourceFile, 'readlines'):        # assume it's a file name
                try:
                    sourceFile = open(os.path.join(self.templateDir, sourceFile))
                    sourceName = sourceFile
                except:
                    self.error(sourceFile, 'could not open file')
            else:
                if hasattr(sourceFile, 'name'):
                    sourceName = sourceFile.name
                else:   # it could be a StringIO or somthin
                    sourceName = '(main template string)'
        elif sourceString:
            sourceFile = StringIO(sourceString)
            sourceName = '(main template string)'

        # load file by lines and recursively expand includes, strip comments
        self.lines = self._preprocessSource(sourceFile, sourceName)

        # compile the loaded template
        self.length = len(self.lines)
        self._compiledLines = [0] * self.length # dummy list because elements won't be assigned in order
        self._compile(0, self.length)


    def merge(self, *data):
        '''
        wrapper around _Merger class, needed for thread safety
        (_Merger instances aren't threadsafe, so we just throw them away after single use)
        '''
        return _Merger(self, *data)._merge()


    def renderValue(self, val):
        '''
        this is a hook in which you can implement all kinds of fancy custom rendering
        for your own objects. The default is just to apply built-in 'str'.
        '''
        return str(val)


    def _preprocessSource(self, sourceFile, sourceName):
        '''
        load file by lines, strip comments, recursively expand include instructions
        keep track of the origin of each line
        '''
        rawLines = sourceFile.readlines()
        sourceFile.close()

        processed = []

        for lineNumber,line in enumerate(rawLines):
            commentStripped = self.commentRegex.sub('', line)
            if not self.stripEmptyLines or commentStripped.strip():
                 processed.append((commentStripped, sourceName, lineNumber))

        # now, check whether we have any include files
        for x in range(len(processed)-1, -1, -1):    # go backwards b/c we will insert more lines
            line = processed[x][0]
            matched = self.includeRegex.match(line)
            if matched:
                includeFileName = matched.group(1)
                fullName = os.path.join(self.templateDir, includeFileName)
                includeFile = open(fullName)
                processed[x:x+1] = self._preprocessSource(includeFile, includeFileName)
        return processed


    def _preprocessPython(self, python):
        '''
        preprocess python statements or expressions to deal with
        interspersed simplified syntax. Helper for _compile.
        '''
        def subst(mo):
            expr = mo.group(1)
            return "_resolveSimple__('%s')" % expr

        isFor = self.forInRe.match(python)
        if isFor:
            forClause, restClause = isFor.group(1), isFor.group(2)
            if self.forInDottedRe.match(forClause):
                self.error(python,
                       "Sorry, Yaptoo cannot handle $-style with dots in loop control variables." + \
                       "Please use explicit Python syntax (e.g use #for x['y'] instead of #for $x.y )"
                          )
            # if we got here, there are no dotted $-style expressions in 'for .. in'
            return forClause.replace('$','') + self.simpleSubstitutionRegex.sub(subst, restClause)
        else:
            return self.simpleSubstitutionRegex.sub(subst, python)

    def _compile(self, i, last):
        '''
        recursively compile the template definition
        '''
        while i < last:
            self.currentLine = i  # needed for error reporting and for caching compiled flow control statements

            line = self.lines[i][0]

            stmt = self.statementRegex.match(line)
            if stmt:
                statement = stmt.group(1)
                firstWord = statement.split()[0]

                if not firstWord in ['if', 'for']:
                    self.error(statement, '%s cannot start a block' % firstWord)

                statementLines = [i]        # record all statements at this level, use as boundaries for recursive compiling

                j = i+1                     # j is the first line contained in this block
                nest = 1                    # count nesting levels of statements

                while j<last:               # look for continuation or end of the block
                    line = self.lines[j][0]
                    stmt = self.statementRegex.match(line)

                    if stmt:
                        followingStatement = stmt.group(1)
                        words = followingStatement.split()

                        if words[0] == 'end':       # found a statement-end
                            nest -= 1

                            if nest == 0:           # this clause ends the current block
                                endWhich = words[1]
                                if endWhich != firstWord:
                                    self.error("Block delimiter mismatch: '%s' / 'end %s'" % (firstWord, endWhich))
                                statementLines.append(j)
                                break

                        elif words[0] in ['if', 'for']:    # begin of a nested statement
                            nest += 1

                        elif nest == 1 and words[0] in ['else:', 'elif']: # look for continuation only at this nesting level
                            if words[0] == 'elif' and firstWord != 'if':
                                self.error("Block delimiter mismatch: '%s' / '%s'" %  (firstWord, words[0]))

                            statementLines.append(j)
                            # create a compound statement ('if elif else', 'for else')
                            statement += '_mergeBlock__(%s,%s)\n%s' % (i+1, j, followingStatement)
                            i = j
                    j += 1

                if nest > 0:
                    self.error(self.lines[self.currentLine], "Missing statement terminator somewhere inside of '%s' block" % firstWord)
                statement += "_mergeBlock__(%s,%s)" % (i+1, j)
                nextLineNo = j+1

                expanded = self._preprocessPython(statement)
                try:
                    compiled = compile(expanded,'<template>','exec')
                    if expanded == statement:
                        self._compiledLines[self.currentLine] = ('exec', (expanded, compiled), nextLineNo)
                    else:
                        self._compiledLines[self.currentLine] = ('exec',
                                    ('%s \nexpanded to:\n%s)' % (statement, expanded),
                                    compiled),
                                nextLineNo)

                except SyntaxError:
                    if expanded != statement:
                        self.error('\n' + expanded, 'Syntax error in flow control statement (expanded from %s)' % statement)
                    else:
                        self.error('\n' + statement, 'Syntax error in flow control statement')

                # now, compile the bits and pieces between the flow control statements of the current block
                for n in range(len(statementLines)-1):
                    startNested, endNested = statementLines[n] + 1, statementLines[n+1]
                    self._compile(startNested, endNested)

                i = nextLineNo


            elif self.faultyStatement.match(line):
                self.error(self.faultyStatement.match(line).group().strip(), 'wrong statement syntax')

            else:       # normal line, copy with substitution. lines can contain
                # - arbitrary python expressions that will be 'evaled'
                # - "$varname.attribute.item.$x" style identifiers
                # -  plain strings

                lineTuples = []     # collect all the constituents of a line as (dispatchKey, funcArg) tuples

                # first, break the line up into marked-up python expressions and intervening strings.
                # this will yield a list that alternatingly contains strings and expressions
                firstFrags = self.expressionRegex.split(line)

                for ff in range(len(firstFrags)):
                    firstItem = firstFrags[ff]

                    if not ff % 2:
                        # even numbers will contain text frags, break them up again to extract the simple-subst. identifiers
                        secondFrags = self.simpleSubstitutionRegex.split(firstItem)

                        for sf in range(len(secondFrags)):
                            item = secondFrags[sf]

                            if not sf % 2 and item: # again, the even numbers will contain plain text
                                lineTuples.append(('text', item))
                            elif sf % 2:   # this is an identifier for simplified syntax substitution.
                                lineTuples.append(('simple', item))

                    else:   # this is a python expression for eval'ing
                        expanded = self._preprocessPython(firstItem)
                        try:
                            compiled = compile(expanded, '<template>', 'eval')
                        except SyntaxError:
                            if expanded != firstItem:
                                self.error(expanded, 'Error compiling Python expression (expanded from %s)' % firstItem)
                            else:
                                self.error(expanded, 'Error compiling Python expression')
                        if expanded == firstItem:
                            lineTuples.append(('eval', (firstItem, compiled)))
                        else:
                            lineTuples.append(('eval',
                                                 ('%s\nexpanded from:\n%s' % (expanded, firstItem),
                                               compiled)))

                self._compiledLines[i] = ('content', lineTuples, i+1)
                i += 1

class _Merger(YaptooErrorHandler):
    '''
    merge a new data set into a compiled template. This class is NOT threadsafe and not intended to be used directly.
    Instead, use Template.merge (which is threadsafe b/c it makes and throws away a fresh _Merger instance on every call).
    '''

    def __init__(self, template, *data):
        '''
        fill the template with a data set and return the string. you may pass one or more dictionaries
        which will be searched on order for the variables in the template.
        '''
        self._t = template
        self._compiledLines = template._compiledLines
        self.renderMissingNames = template.renderMissingNames   # needed by ErrorHandler
        self.renderMissingFormat = template.renderMissingFormat
        self.lines = template.lines

        self.globals = {}
        for x in range(len(data)-1, -1, -1):  # update in reverse order to achieve 'search list' behaviour
            self.globals.update(data[x])

        # add some magic to the global namespace, needed by compiled exec-statements
        self.globals['_mergeBlock__'] = self._mergeBlock
        self.globals['_resolveSimple__'] = self._resolveSimple

        # append output here
        self.out = []

        # method switchers
        self.lineDispatch = {                            # deal with the items that make up a line
                            'text'   : self.out.append,
                            'eval'   : self._evalSubst,
                            'simple' : self._simpleSubst,
                        }

        self.blockDispatch = {                           # deal with the various lines in a block
                            'content': self._mergeLine,
                            'exec'   : self._execute,
                        }

    def _merge(self):
        '''
        Don't use directly - use Template.merge instead
        '''
        self._mergeBlock(0, self._t.length)
        return self.postProcess(''.join(self.out))

    def _mergeBlock(self, first, last):
        '''
        merge a block of lines. Helper for merge.
        '''
        lineNumber = first
        while lineNumber < last:
            self.currentLine = lineNumber
            instruction, args, lineNumber = self._compiledLines[lineNumber]
            self.blockDispatch[instruction](args)   # this will call '_execute' or '_mergeLine'

    def _execute(self, execStuff):
        '''
        execute a precompiled flow control statement. Helper for merge.
        '''
        execStatement, compiled = execStuff
        try:
            exec compiled in self.globals
        except YaptooError:
            raise       # let errors from nested code propagate, as they have already been annotated
        except:         # error was caused here
            self.error('\n'+execStatement, 'Error while executing compiled flow control statement')

    def _mergeLine(self, lineTuples):
        '''
        merge a previously compiled content (as opposed to flow control) line.
        Called via blockDispatch['content']
        '''
        for key, funcArg in lineTuples:
            self.lineDispatch[key](funcArg) # this will call out.append, _evalSubst, or _simpleSubst

    def _evalSubst(self, tup):
        '''
        eval an arbitrary Python exp and insert the value
        '''
        try:
            val = eval(tup[1], self.globals)
        except: # tell user what occurred and where
            if self.renderMissingNames:
                val = self.renderMissingFormat % tup[0]
            else:
                self.error(tup[0], "Error while eval'ing compiled Python expression")
        if val == None:
            val = ''
        self._renderValue(val)


    def _simpleSubst(self, expr):
        '''
        resolve an expression like '$hans.wurst.senf' and append its value to the output
        this is used from outside statements and expressions
        '''
        try:
            val = self._resolveSimple(expr)
        except: # tell user what occurred and where
            if self.renderMissingNames:
                val = self.renderMissingFormat % ('$' + expr)
            else:
                raise
        self._renderValue(val)


    def _resolveSimple(self, expr):
        '''
        resolve $-style expressions
        '''
        frags = expr.split('.')

        try:
            resolved = self.globals[frags[0]]
        except KeyError:
            self.error(frags[0], 'missing name %s' % frags[0])

        for i in range(1, len(frags)):
            frag = frags[i]

            if frag.startswith('$'):    # refers to a global variable
                frag = frag[1:]         # cut it off...
                isGlobal = True
                try:
                    term = self.globals[frag]
                except KeyError:
                    self.error(frag, 'missing name %s' % frag)
            else:
                isGlobal = False
                term = frag

            try:
                kid = resolved[term]
                # o.k., it's there...
            except TypeError:
                self.error(expr, "\nTried to look up key '%s' in wrong type of container '%s'" % (frag, frags[i-1]))

            except (KeyError, AttributeError):
                if not isGlobal:
                    try:    # second, try to get it as an attribute
                        kid = getattr(resolved, frag)
                        # no, it's here...
                    except AttributeError:
                        self.error(expr, "\nCan't find item or attribute '%s' in '%s'" % (frag, '.'.join(frags[:i])))
                else:
                    self.error(expr, "\nCan't find item '%s' in '%s'" % (frag, '.'.join(frags[:i])))

            resolved = kid    # repeat for next round

        return resolved

    def _renderValue(self, val):
        '''
        wrapper for Template.renderValue
        '''
        self.out.append(self._t.renderValue(val))

    def postProcess(self, bigString):
        '''
        apply last-ditch changes to the merged output string.
        for now, just throw out the line joiners with their newlines
        '''
        return self._t.joinLines.sub('', bigString)


#########################################################
if __name__ == '__main__': # simple usage demonstration

    tmpl='''
    <html>
    <body>
    #include includeTest.tmpl
    <table>
    #for $x, $y in $rows:
        <tr><td>$x</td><td>$y</td></tr>
    #end for
    #for $key in $theDict:
        <tr><td>$key</td><td>$theDict.$key</td></tr>
    #end for
    #for $row in $listOfDicts:
      #if 'Nickname' in $row:
        <tr><td>$row.FirstName</td><td>$row.Nickname</td></tr>
      #end if
    #end for
    </table>
    </body>
    </html>
    '''
    def test():
        rows = [('spam', 'eggs'), ('more spam', 'more eggs')]
        theDict = {'some':'spam and eggs', 'more':'more spam and eggs'}
        listOfDicts = [
            {'FirstName':'Uwe', 'LastName':'Seeler', 'Nickname':'Uns Uwe'},
            {'FirstName':'Gerd', 'LastName':'Mueller', 'Nickname':'Der Bomber'}
        ]

        t = Template(sourceString=tmpl)
        return t.merge(locals())

    print test()
