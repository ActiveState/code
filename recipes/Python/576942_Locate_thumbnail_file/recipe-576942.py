"""Get the thumbnail stored on the system.
Should work on any linux system following the desktop standards"""

import hashlib
import os

def get_thumbnailfile(filename):
    """Given the filename for an image,
    return the path to the thumbnail file.
    Returns None if there is no thumbnail file.
    """
    # Generate the md5 hash of the file uri
    file_hash = hashlib.md5('file://'+filename).hexdigest()

    # the thumbnail file is stored in the ~/.thumbnails/normal folder
    # it is a png file and name is the md5 hash calculated earlier
    tb_filename = os.path.join(os.path.expanduser('~/.thumbnails/normal'),
                               file_hash) + '.png'
    if os.path.exists(tb_filename):
        return tb_filename
    else:
        return None

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'Usage ---'
        print ' get_thumbnail.py filename'
        sys.exit(0)
        
    filename = sys.argv[1]
    tb_filename = get_thumbnailfile(filename)
    
    if tb_filename:
        print 'Thumbnail for file %s is located at %s' %(
            filename, tb_filename)
    else:
        print 'No thumbnail found'
