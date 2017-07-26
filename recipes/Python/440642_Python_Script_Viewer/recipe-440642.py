import cgi

def main():
    if cgi.dictionary is None or not cgi.dictionary.has_key('file'):
        show_form()
    else:
        show_file()

def show_form(error = ''):
    if error != '':
        error = '\t\t\t' + error + ' cannot be displayed.<br>\n'
    cgi.html('''<html>
\t<head>
\t\t<title>
\t\t\tPython Script Viewer
\t\t</title>
\t</head>
\t<body>
\t\t<form action="python_script_viewer.py">\n''' + error + '''\t\t\tPython Script Filename:<br>
\t\t\t<input type="text" name="file" size="50"><br>
\t\t\t<input type="submit" value="Display">
\t\t</form>
\t</body>
</html>''')

def show_file():
    try:
        if cgi.dictionary['file'][-3:].lower() != '.py':
            raise Exception
        cgi.plain(file(cgi.dictionary['file']).read())
    except:
        show_form(cgi.dictionary['file'])

if __name__ == '__main__':
    cgi.execute(main, 'python')
