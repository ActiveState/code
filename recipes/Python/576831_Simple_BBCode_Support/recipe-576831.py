class _BBCode:

    def __getattr__(self, name):
        method = _Virtual(name)
        setattr(self, name, method)
        return method

class _Virtual:

    def __init__(self, name):
        self.__name = name.upper()

    def __call__(self, string, *args):
        return '[{0}{1}]{2}[/{0}]'.format(self.__name, ('=' + ','.join(map(str, args))) if args else '', string)

BBCode = _BBCode()

################################################################################

# EXAMPLE FOLLOWS

BBCode.b('A bold sentence')
'[B]A bold sentence[/B]'

>>> BBCode.i('Italics')
'[I]Italics[/I]'

>>> BBCode.u('underline')
'[U]underline[/U]'

>>> 'I want one ' + BBCode.s('million') + ' billion dollars'
'I want one [S]million[/S] billion dollars'

>>> BBCode.sub('sub') + 'marine'
'[SUB]sub[/SUB]marine'

>>> 'x' + BBCode.sup(2)
'x[SUP]2[/SUP]'

>>> BBCode.big('big')
'[BIG]big[/BIG]'

>>> BBCode.big(BBCode.big('bigger'))
'[BIG][BIG]bigger[/BIG][/BIG]'

>>> BBCode.small('smaller text')
'[SMALL]smaller text[/SMALL]'

>>> BBCode.color('Green text', 'green')
'[COLOR=green]Green text[/COLOR]'

>>> BBCode.bgcolor('A background for text', 'lightgreen')
'[BGCOLOR=lightgreen]A background for text[/BGCOLOR]'

>>> BBCode.border('bordered', 'red')
'[BORDER=red]bordered[/BORDER]'

>>> BBCode.border('bordered', 'blue', 3)
'[BORDER=blue,3]bordered[/BORDER]'

>>> BBCode.border('bordered', 'green', 1, 'dotted')
'[BORDER=green,1,dotted]bordered[/BORDER]'

>>> BBCode.center('centered')
'[CENTER]centered[/CENTER]'

>>> BBCode.right('right aligned')
'[RIGHT]right aligned[/RIGHT]'

>>> BBCode.font('A different font', 'verdana')
'[FONT=verdana]A different font[/FONT]'

>>> BBCode.quote('Party time', 'Joe')
'[QUOTE=Joe]Party time[/QUOTE]'

>>> BBCode.quote('Party time')
'[QUOTE]Party time[/QUOTE]'

>>> print(BBCode.html('''<html>
<head>
<title>Steel Headquarters</title>
</head>
<body>
<p class="intro">Welcome</p>
</body>
</html>'''))
[HTML]<html>
<head>
<title>Steel Headquarters</title>
</head>
<body>
<p class="intro">Welcome</p>
</body>
</html>[/HTML]

>>> BBCode.nocode('lets show someone how to make text bigger ' + BBCode.big('bigger text'))
'[NOCODE]lets show someone how to make text bigger [BIG]bigger text[/BIG][/NOCODE]'

>>> BBCode.code('''int x = y;
x++;''')
'[CODE]int x = y;\nx++;[/CODE]'

>>> BBCode.url('Google', 'http://www.google.com/')
'[URL=http://www.google.com/]Google[/URL]'

>>> BBCode.url('http://www.google.com/')
'[URL]http://www.google.com/[/URL]'

>>> BBCode.img('http://www.google.com/logos/july4th09.gif')
'[IMG]http://www.google.com/logos/july4th09.gif[/IMG]'

>>> BBCode.email('Email me', 'user@example.com')
'[EMAIL=user@example.com]Email me[/EMAIL]'

>>> BBCode.email('user@example.com')
'[EMAIL]user@example.com[/EMAIL]'

>>> BBCode.flash('http://www.youtube.com/v/z7SeHqxOVYc', 250, 210)
'[FLASH=250,210]http://www.youtube.com/v/z7SeHqxOVYc[/FLASH]'

>>> BBCode.list(''.join(map(lambda item: '[*]' + item, ('Item 1', 'Item 2', 'Item 3'))))
'[LIST][*]Item 1[*]Item 2[*]Item 3[/LIST]'

>>> BBCode.list(''.join(map(lambda item: '[*]' + item, ('Item 1', 'Item 2', 'Item 3'))), 1)
'[LIST=1][*]Item 1[*]Item 2[*]Item 3[/LIST]'

>>> 'You may want to hide something from accidental viewing:' + BBCode.spoiler('or the secret may be spoiled')
'You may want to hide something from accidental viewing:[SPOILER]or the secret may be spoiled[/SPOILER]'

>>>

################################################################################

# EXAMPLE PATCH

class _Patch(_BBCode):

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def bulleted(self, *items):
        return '[LIST]' + ''.join(map(lambda item: '[*]' + item, items)) + '[/LIST]'

    def numbered(self, *items):
        return '[LIST=1]' + ''.join(map(lambda item: '[*]' + item, items)) + '[/LIST]'

#############################################

>>> BBCode = _Patch(SELF='[me]', RULE='[hr]')

>>> BBCode.bulleted('Item 1', 'Item 2', 'Item 3')
'[LIST][*]Item 1[*]Item 2[*]Item 3[/LIST]'

>>> BBCode.numbered('Item 1', 'Item 2', 'Item 3')
'[LIST=1][*]Item 1[*]Item 2[*]Item 3[/LIST]'

>>> BBCode.SELF
'[me]'

>>> BBCode.RULE
'[hr]'

>>>
