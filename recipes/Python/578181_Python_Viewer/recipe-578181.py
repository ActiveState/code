import os
import sys
import Zcgi

def main():
    if Zcgi.dictionary is None or not Zcgi.dictionary.has_key('file'):
        show_form()
    else:
        show_file()

def show_form(error=''):
    if error:
        error = '\t\t\t<b>' + error + '</b> cannot be displayed.<br>\n'
    Zcgi.print_html('''<html>
\t<head>
\t\t<title>
\t\t\tPython Script Viewer
\t\t</title>
\t</head>
\t<body>
\t\t<form action="%s">
%s\t\t\tPython Script Filename:<br>
\t\t\t<input type="text" name="file" size="50"><br>
\t\t\t<input type="submit" value="Display">
\t\t</form>
\t</body>
</html>''' % (os.path.basename(sys.argv[0]), error))

def show_file():
    try:
        if Zcgi.dictionary['file'][-3:].lower() != '.py':
            raise Exception
        Zcgi.print_plain(file(Zcgi.dictionary['file']).read())
    except Exception, error:
        if error.__class__ is not SystemExit:
            show_form(Zcgi.dictionary['file'])

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')
