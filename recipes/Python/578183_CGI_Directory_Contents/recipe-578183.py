import os, Zcgi

def main():
    dirs = []
    files = []
    others = []
    for name in os.listdir(os.getcwd()):
        path = os.path.join(os.getcwd(), name)
        if os.path.isdir(path):
            dirs.append(name)
        elif os.path.isfile(name):
            files.append(name)
        else:
            others.append(name)
    text = underline('Current Directory Contents:')
    if len(dirs):
        text += '\n\n' + underline('Directories:')
        for name in dirs:
            text += '\n' + name
    if len(files):
        text += '\n\n' + underline('Files:')
        for name in files:
            text += '\n' + name
    if len(others):
        text += '\n\n' + underline('Others:')
        for name in others:
            text += '\n' + name
    Zcgi.print_plain(text)

def underline(string):
    return string + '\n' + '=' * len(string)

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')
