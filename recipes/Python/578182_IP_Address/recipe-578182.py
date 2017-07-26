import os, Zcgi

def main():
    text = '''<html>
\t<head>
\t\t<title>
\t\t\tWho am I?
\t\t</title>
\t</head>
\t<body>
\t\t<b>
\t\t\t'''
    try:
        text += 'You are ' + os.environ['REMOTE_ADDR'] + '.'
    except:
        text += 'I do not know.'
    text += '''
\t\t</b>
\t</body>
</html>'''
    Zcgi.print_html(text)

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')
