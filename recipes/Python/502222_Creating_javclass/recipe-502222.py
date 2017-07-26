#!/usr/bin/env jython
from java.lang import Class, UnsatisfiedLinkError, NoClassDefFoundError, \
     InstantiationException, System, StringIndexOutOfBoundsException
from types import StringType, UnicodeType
from org.python.core import PyJavaPackage
from string import join, split
import com, org, sun, java, javax, re
from java.lang.reflect import Modifier
from string import join, lower

def classCss(indents):
    """return Casscation Style Sheet."""
    css = 'li, ul, o, p{padding: 0; margin: 0;}\nul{margin:0.5em 0 0.5em 0}\nh'
    css += '1, h2{text-align: center; font-family:Time; font-weight: normal}\n'
    css += 'h1{ font-size: 18pt; }\nh2{ font-size: 14pt; }\nli, p{ font-family'
    css += ': Courier New; font-size: 10pt;}\nli{ list-style-type:none; margin'
    css += ':0.5em 0 0.5em 0}\n'
    for i in range(indents):
        css += 'ul.ind%i li{ text-indent: %iem; }\n' % (i, (i+1)*4)
    return css

def baseHtml(title, body):
    """return base html document with css style."""
    html = '<html>\n<head>\n<title>%s</title>\n<link href="class.css" type="te'
    html += 'xt/css" rel="stylesheet"/>\n</head>\n<body>\n%s\n</body>\n</html>'
    return html % (title, body)

def frameSet():
    """return frameset html page."""
    html = '<html>\n<head>\n<title>Java Class Index</title>\n</head>\n<framese'
    html +='t cols="30%,70%">\n    <frame src="start.html" name="tree" title="'
    html +='class Tree">\n    <frame name="packgeMember" title="Class, interfa'
    html +='ce or package">\n</frameset>\n</html>'
    return html

javaKeywords = ('void', 'private', 'public', 'protected', 'final', 
                'static', 'int', 'float', 'boolean', 'native', 'throws',
                'interface', 'class', 'abstract', 'extends', 'implements')
                       
def boldJavaKeywords(str):
    """return copy of the string with html bolded java keywords."""
    for i in javaKeywords:
        str = re.sub(r'(>|\s){1}%s(<|\s){1}' % i, r'\1<b>%s</b>\2' % i, str)
    return str.replace('</b> <b>', ' ')
    

def li(lst):
    """return list of li html tags."""
    return ['<li>%s</li>' % element for element in lst]

def tag(name, content, **atr):
    """return string containing html tag."""
    return '<%s %s>%s</%s>' % (name, atributes(**atr), content, name)

def atributes(**kwargs):
    """return dictionary as html formated atributes."""
    return join(['%s="%s"' % (lower(k),v) for k, v in kwargs.iteritems()])

def ul(cls, lst):
    """create html ul from list with class cls"""
    result = ['<ul class="%s">' % (cls)]
    result += ['%s%s' % (' '*4, l) for l in li(lst)]
    result += ['</ul>']
    return result

def List(lst, type_, **kwargs):
    """create html ul from list with class cls"""
    result = ['<%s %s>' % (type_, atributes(**kwargs))]
    result += [(' '*4) + tag('li', elem) for elem in lst]
    result += ['</%s>' % (type_)]
    return result

def classLink(className, string_):
    """return copy of string with className replaced by HTML link to it."""
    classN = re.sub(r'((\w+\.)+(\w+))', r'\3', className)
    result = string_.replace(className, classN)
    return re.sub(r'((\w+\.)+(\w+))', r'<a href="\1.html">\3</a>', result)

def membersToHtml(getMembers, ind=1):
    """return html list od members retrived from getMember function."""
    classPath = r' (\w+[\.|\$])+%s'
    list_ = ''
    indent = (' '*(ind+2)*4)
    for i in getMembers():
        name = i.getName()
        cleared = re.sub(classPath % name, ' %s' % name, i.toString())
        list_ += '%s<li>%s;</li>\n' % (indent, cleared)
    return list_

def javaClassToHtml(javaClass, level=0):
    """return html class representation."""
    if type(javaClass) is StringType or type(javaClass) is UnicodeType:
        class_ = Class.forName(javaClass)
        className = javaClass
    else:
        class_ = javaClass
        className = javaClass.__name__
    if Class.isInterface(class_):
        typeStr = 'interface'
    elif Modifier.isAbstract(Class.getModifiers(class_)):
        typeStr = 'abstract class'
    else:
        typeStr = 'class'
    #indent = (' '*level+1)*4)
    indent = ' '*(level+1)*4
    header = '%s<p>%s %s' % (indent, typeStr, className)
    super_ = Class.getSuperclass(class_)
    if super_ is not None:
        header += ' extends ' + Class.getName(super_)
    interfaces = Class.getInterfaces(class_)
    if len(interfaces) > 0:
        interfacesNames = join(map(Class.getName, interfaces), ', ')
        header += ' implements %s' % (interfacesNames)
    body = membersToHtml(lambda: Class.getDeclaredFields(class_), level)
    body += membersToHtml(lambda: Class.getDeclaredConstructors(class_), level)
    body += membersToHtml(lambda: Class.getDeclaredMethods(class_), level)
    body = '%s{</p>\n%s<ul class="ind%i">\n%s' % (header, indent, level, body)
    body = boldJavaKeywords(classLink(className, body))
    li = '%s<li>\n%s\n%s</li>\n'
    ind2 = (' '*(level+2)*4)
    for cl in Class.getDeclaredClasses(class_):
        body += li % (ind2, javaClassToHtml(Class.getName(cl), level+1), \
                indent*2)
    return '%s%s</ul>}' % (body, indent)


def toFile(fileName, content):

    """safe file writing"""
    f = open(fileName, 'w+')
    f.write(content)
    f.close()
    f = None

classSaved = []

def classToFile(className):
    """save html class representation to file <className>.html."""
    global classSaved
    if className not in classSaved:
        print '    creating %s.html' % className
        packageName = Class.getPackage(Class.forName(className)).getName()
        packageLnk = '<a href="%s.html">%s</a>' % (packageName, packageName)
        htmlClass = '    <h1>Class <b>%s</b> from package %s</h1>' % \
                    (className, packageLnk)
        htmlClass += '\n' + javaClassToHtml(className)
        htmlContent = baseHtml(className, htmlClass)
        toFile('%s.html' % className, htmlContent)
        classSaved += [className]
    else:
        print '    file %s.html was writen allready' % (className)

def isjpackage(object_):
    """return true if object_ is PyjavaPackage."""
    return type(object_) is PyJavaPackage

def isjclass(object_):
    """return true if object_ is PyJavaClass."""
    return type(object_) is not PyJavaPackage

def dirPackage(package):
    """return a dictionary {'package Name': PyJavaPackage}."""
    return [getattr(package, name) for name in dir(package) if not re.match('__[^_]+__', name)]

def filter_package_content(package, fun):
    """return filtered package content."""
    packageContent = dirPackage(package)
    filtered = [p.__name__ for p in filter(fun, packageContent)]
    return filtered

def packageToHmtl(package):
    """return html for package content.

    it use better technic than javaClassToFile
    """
    packageContent = dirPackage(package)
    lst = [tag('h1', 'Package %s' % tag('b', '%s' % (package.__name__)))]
    lnkClass = tag('a', '%s',  target='packgeMember', href='%s.html')
    lnkPkg = tag('a', '%s', href='%s.html')
    pack = [p.__name__ for p in filter(isjpackage, packageContent)]
    if len(pack):
        lst += [tag('h2', 'package list:')]
        lst += List([lnkPkg % (p,p) for p in pack], 'ul', Class='ind0')
    classes = [p.__name__ for p in filter(isjclass, packageContent)]
    if len(classes):
        lst += [tag('h2', 'class list:')]
        linkList = [lnkClass % (p,p) for p in classes]
        lst += List(linkList, 'ul', Class='ind0')
    return baseHtml(package.__name__, join(lst, '\n%s' % (' '*4)))

def packageToFile(package):
    """save package to file."""
    print '    creating package file %s.html' % (package.__name__)
    toFile('%s.html' % (package.__name__), packageToHmtl(package))


def classList():
    result += classList(p, ind+1)


def classTraverse(package, classFun, packageFun):
    """traverse package with classFun and packageFun."""
    for member in filter(lambda name: not re.match('__[^_]+__', name), dir(package)):
        print repr(member)
        try:
            memberObject = getattr(package, member)
            if isjpackage(memberObject):
                packageFun(memberObject)    # use packageFun to PyJavaPackage
                classTraverse(memberObject, classFun, packageFun)
            elif isjclass(memberObject):
                classFun(memberObject)      # use classFun to PyjavaClass
        except NoClassDefFoundError:
            print 'EXCEPTION: can\'t found package'
        except InstantiationException:
            print 'EXCEPTION: can\'t create package intance'
        except StringIndexOutOfBoundsException:
            print 'EXCEPTION: StringIndexOutOfBoundsException'
        except UnsatisfiedLinkError:
            print 'EXCEPTION: UnsatisfiedLinkError for package'


def usage():
    print 'usage:'
    print '     jython class.py (<class> | <package> | all | index)'
    print ''
    print '     class and package names must have dot notation'
    print '      eg. javax.swing.JApplet'

def main():
    from sys import argv
    if len(argv) == 2:
        classToFiles = lambda x: classToFile(x.__name__)
        if argv[1] == 'all':
            # traverse throught all listed packages
            for package in [com, java, javax, org]: # sun
                print 'proceed package', package.__name__
                packageToFile(package)
                classTraverse(package, classToFiles, packageToFile)
                System.gc()
            print 'writen ', len(classSaved), ' files'
            while len(classSaved) != 0:
                del classSaved[0]
        elif argv[1] == 'packages':
            for package in [com, java, javax, org]:
                print 'proceed package', package.__name__
                packageToFile(package)
                classTraverse(package, lambda x: None, packageToFile)
                System.gc()
        elif argv[1] == 'css':
            toFile('class.css', classCss(2))
        elif argv[1] == 'index':
            print 'creating index.html'
            toFile('index.html', frameSet())
            lnk = '<a href="%s.html">%s</a>'
            packages = [com, java, javax, org ]
            links = [lnk % (p.__name__,p.__name__) for p in packages]
            start = ['<h1>(JYTHON) CLASS</h1>'] + ['<ul>']
            start += ul('ind0', links)
            start += ['</ul>']
            html = join(start, (' '*4)+'\n')
            print 'creating start.html'
            toFile('start.html', baseHtml('javaDoc', html))
        else:
            arg = eval(argv[1])
            if type(arg) == PyJavaPackage:
                classTraverse(arg, classToFileS, packageToFile)
            elif type(arg) != PyJavaPackage:
                classToFile(argv[1])
            else:
                usage()
    else:
        usage()

if __name__ == '__main__':
    main()
