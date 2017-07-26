'''
Server-side javascript dependency resolution
'''

import os, os.path, re, fnmatch

try:
    set
except NameError:
    from sets import Set as set

class JSResolverError(Exception):
    pass


class _JSFile(object):
    '''
    Helper class for JSResolver
    '''
    noWordRe = re.compile('\W+')
    default_extension = '.js'               # auto-complete script names without extension
    declarationPhrase = 'requireScript'     # declare dependencies like so: // requireScript bob.js, jack.js, lizzy.js

    def __init__(self, root, path, filename):
        self.root = root
        self.path = path
        self.name = filename
        self.relpath = os.path.join(self.path, self.name)
        self.fullpath = os.path.join(self.root, self.relpath)

    def read(self):
        '''
        read the file contents
        '''
        f = open(self.fullpath)
        text = f.read()
        f.close()
        return text

    def age(self):
        '''
        get the file age - useful for setting LastMod headers
        '''
        return os.stat(self.fullpath)[8]

    def declaredDependencies(self):
        '''
        flat list of all js modules we have been declared to depend on.
        no actual resolution done here.
        '''
        deps = set() # make this a set in order to eliminate repetitions
        def autocomplete(name):
            if '.' in name: return name
            return name + self.default_extension

        for line in self.read().splitlines():
            line = line.strip()
            if line.startswith('//'):
                words = filter(None, self.noWordRe.split(line))
                if words and words[0] == self.declarationPhrase:
                    scripts = [ autocomplete(x) for x in words[1:] ]
                    deps |= set(scripts)
        return deps


class JSResolver(object):
    '''
    Main class. Instantiate with the root directory of your JavaScript files.
    '''

    extSplit = re.compile('\s*[\;\,]\s*')   # break up a string across ',' or ';'

    def __init__(
                 self,
                 js_root,                     # file system path of the js root directory
                 js_patterns = '*.js',        # the javascript source file names must have one of these extensions
                 preresolve = True            # pre-resolve all files under js_root
                ):

        self.js_patterns = self.extSplit.split(js_patterns)
        self.js_root = js_root

        # detect repeated resolution attempts - these indicate some circular dependency
        self.reentrantResolution = set()

        # for each script, keep a set of dependencies
        self.dependencies = {}

        # collect all javascript files underneath root directory
        self.files = {}

        rawFiles = self._all_files(js_root)
        for path, filename in rawFiles:
            newf = _JSFile(js_root, path, filename)
            oldf = self.files.get(filename)
            if oldf:    # ambiguity - don't guess what the user wanted...
                raise JSResolverError, 'file %s occurs twice(%s and %s)' % (filename, oldf.relpath, newf.relpath)
            self.files[filename] = newf

        # resolve dependencies in all loaded files. Benefit: thread safety -
        # once everything is resolved, there will be no more state changes
        # also, it is better to upchuck and die directly upon server start
        # than only later upon request of a faulty script
        if preresolve:
            for fn in self.files.keys():
                self._resolve(fn)


    def _all_files(self, root):
        '''
        helper for __init__: recurse over js root directory and collect all js files
        '''
        rv = []
        old = os.getcwd()
        os.chdir(root)

        for path, subdirs, files in os.walk('.'):
            for name in files:
                for pattern in self.js_patterns:
                    if fnmatch.fnmatch(name, pattern):
                        path = os.path.normpath(path)
                        if path == '.':
                            path=''
                        rv.append((path, name))
        os.chdir(old)
        return rv


    def _resolve(self, scriptName, foundInScript = None):
        '''
        the center piece.
        recursively resolve dependencies of scripts
        return them as a flat list, sorted according to ancestral relationships
        '''
        resolved = self.dependencies.get(scriptName, None)
        if resolved is not None:
            return resolved

        scriptFile = self.files.get(scriptName)

        if not scriptFile:
            msg = 'script %s not found' % scriptName
            if foundInScript:
                msg += ' while resolving %s' % foundInScript
            raise JSResolverError, msg

        declared = scriptFile.declaredDependencies()

        resolved = set()

        for decl in declared:
            resolutionStep = (scriptName, decl)
            if resolutionStep in self.reentrantResolution:
                if foundInScript:
                    scapegoat = foundInScript
                else:
                    scapegoat = decl
                raise JSResolverError, 'circular dependency involving %s and %s' % (scriptName, scapegoat)
            self.reentrantResolution.add(resolutionStep)
            # resolved.add(decl)      # add the declared script ...
            resolved.update(self._resolve(decl, foundInScript = scriptName)) # and its dependencies, if any

        resolved = list(resolved)
        # now it's time for sorting hierarchically... Since circular dependencies are excluded,
        # ancestors will always have fewer dependencies than descendants, so sorting by the
        # number of dependencies will give us the desired order.
        resolved.sort(key = lambda x : len(self.dependencies[x]))
        resolved.append(scriptName)
        self.dependencies[scriptName] = resolved
        return resolved

    def _resolvedFiles(self, scriptName):
        '''
        simple auxiliary - lookup the _JSFile instances for file names
        '''
        return [self.files[x] for x in self._resolve(scriptName)]

    def asNames(self, scriptName):
        '''
        simply return the names of the files we depend on, in order
        '''
        resolved = self._resolvedFiles(scriptName)
        return [r.relpath for r in resolved]

    def asNamesAndAges(self, scriptName):
        '''
        names and file ages - use this to set headers
        question is, for what? only if we want to send the big blurb would we need it...
        Only for some primitive server maybe that doesn't automatically send the appropriate
        headers.
        '''
        resolved = self._resolvedFiles(scriptName)
        return [(r.relpath, r.age()) for r in resolved]

    def asTags(self, scriptName, baseUrl='', indent=0):
        '''
        return a list of <script> tags for inclusion in a HTML page
        '''
        resolved = self._resolvedFiles(scriptName)
        out = []
        for r in resolved:
            out.append("%s<script language='javascript' src='%s%s'></script>" % (' ' * indent, baseUrl, r.relpath))
        return '\n'.join(out)

    def asMerged(self, scriptName):
        '''
        merge all files into one big file. Not as practical as you might think - will prevent reuse of
        js files across multiple page of the same site if some of the files differ.
        Neveurtheless, sometimes it may be useful.
        '''
        resolved = self._resolvedFiles(scriptName)

        outList = []
        for sc in resolved:
            ancestorNames = self.dependencies[sc.name][:-1] # cut off the script itself
            if ancestorNames:
                ancestorNames.sort(key = str.lower)
                dpstr = 'requires: %s' % ', '.join(ancestorNames)
            else:
                dpstr = 'no dependencies'

            title = 'Start of %s (%s) *' % (sc.name, dpstr)
            outList.append('\n/*' + '*' * (len(title) + 0))
            outList.append('* %s' % title)
            outList.append('%s/' % ('*' * (len(title) + 1)))
            outList.append(sc.read())

        # determine age (from that of most recently changed file)
        age = max([s.age() for s in resolved])
        return ('\n'.join(outList), age)



if __name__ == '__main__':

    j = JSResolver('/home/joe/blow/js/')

    for k in j.dependencies.keys():
        print j.asTags(k)
        print
