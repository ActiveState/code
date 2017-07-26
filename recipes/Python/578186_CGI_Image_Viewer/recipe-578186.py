# INCOMPLETE

from cPickle import dump, load
from os import basename
from os.path import exists, isdir, join
from sys import argv
from Zcgi import *

image_extentions = '.bmp', '.gif', '.jpg', '.png'

def main():
    # Default Settings
    title = 'Image Viewer'
    image = ''
    action = basename(argv[0])
    back = ''
    forward = ''
    hidden = ''
    if dictionary is None:
        # Nothing To Do
        pass
    elif dictionary.had_key('directory'):
        # Something To Do
        if not dictionary.has_key('hidden'):
            # Just Began Viewing
            if isdir(dictionary['directory']):
                # Check For Pickle
                image_pickle = join(dictionary['directory'], 'image.pickle')
                if exists(image_pickle):
                    # Load Directory Listing
                    dir_data = load(file(image_pickle))
                else:
                    # Create Directory Listing
                    dir_data = update_image_pickle(dictionary['directory'])
                    # START HERE
                image = WHAT_TO_DECIDE_HERE
            else:
                # Post Error Message
                dictionary['directory'] = 'No Such Directory'
        else:
            # Find Next Image
    show_form(title, image, action, back, forward, hidden)

def show_form(*form_settings):
    print_html('''<html>
\t<head>
\t\t<title>
\t\t\t%s
\t\t</title>
\t</head>
\t<body>
\t\t<center>%s
\t\t\t<form action="%s">
\t\t\t\t<input type="text" name="directory" size="50"><br>
\t\t\t\t%s<input type="submit" name="browse" value="Browse">%s%s
\t\t\t</form>
\t\t</center>
\t</body>
</html>''' % form_settings)
