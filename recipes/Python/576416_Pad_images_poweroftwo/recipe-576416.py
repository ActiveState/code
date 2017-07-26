#!/usr/bin/env python
'''Takes any number of images and pads them to be power of two dimensions.

For example: ImageA.png is a 23x10 image.  After being run through
convert_to_POT, it will be the same size centered in a transparent 32x16
canvas.  NOTE: Does not work with palette (ie. '.gif') images.

'''

__author__ = "Martin Wilson: martinmwilson@gmail.com"

import sys
import os
import logging

class PotException(Exception):
    '''Base exception for this module.'''
    pass
class PotArgumentError(PotException): 
    '''Used if a function is passed invalid arguments.'''
    pass


def get_dimensions(size, pots):
    '''Returns closest greater or equal than power-of-two dimensions.
    
    If a dimension is bigger than max(pots), that dimension will be returned
    as None.
    
    '''
    width, height = None, None
    for pot in pots:
        # '<=' means dimension will not change if already a power-of-two
        if size[0] <= pot:
            width = pot
            break
    for pot in pots:
        if size[1] <= pot:
            height = pot
            break
    return width, height


def get_color(mode, image_file, color):
    '''Returns padding color that matches the mode of the original image.
    
    Retuns None if the original image was not an RGB or RGBA image.
    
    '''
    if mode.upper() == "RGBA":
        out_color = color
    elif mode.upper() == "RGB":
        if color[3] == 255:
            logging.info("'%s' not RGBA, falling back to black border..." %
                         (os.path.basename(image_file)))
        out_color = color[0:2]
    else:
        return None
    return out_color


def convert(files, overwrite=False, extension=None, color=(0, 0, 0, 0)):
    '''Takes a list of files and pads each one to power-of-two dimensions.'''
    try:
        from PIL import Image
    except ImportError:
        logging.error("You must install the Python Imaging Library to use " + 
                      "this script.")
        sys.exit(1)

    # ---Validating arguments---
    if overwrite and extension:
        raise PotArgumentError("'overwrite' and 'extension' cannot both be "+
                               "passed.")
    elif not overwrite and not extension:
        raise PotArgumentError("Must pass either overwrite or extension.")
    elif not overwrite and not isinstance(extension, basestring):
        raise PotArgumentError("Extension must be string.")
    if len(color) != 4 or not (isinstance(color, list) or 
                               isinstance(color, tuple)):
        raise PotArgumentError("'color' must be length 4 tuple or list.")

    # ---Image manipulation---
    pots = [2 ** exp for exp in range(16)] #powersoftwo
    for image_file in files:
        image = Image.open(image_file)

        # ---Deciding new dimensions---
        width, height = get_dimensions(image.size, pots)
        if width == None or height == None:
            logging.warning("'%s' has too large dimensions, skipping." % 
                            os.path.basename(image_file))
            continue

        # ---Checking for transparency support---
        out_color = get_color(image.mode, image_file, color)
        if out_color == None:
            logging.warning("'%s' not an RGB or RGBA image, skipping." % 
                            os.path.basename(image_file))
            continue

        # ---Creating output---
        logging.info("'%s' is %dx%d, making new %dx%d image..." % 
                     (os.path.basename(image_file), image.size[0],
                      image.size[1], width, height))
        output = Image.new(image.mode, (width, height), out_color)
        output.paste(image, ((width - image.size[0]) / 2, 
                             (height - image.size[1]) / 2))
        # Be able to write new file with same mode as old file
        mode = os.stat(image_file).st_mode
        # ---Saving output---
        if overwrite:
            output.save(image_file, image.format)
            os.chmod(image_file, mode)
        else:
            image_file = os.path.splitext(image_file)
            output_file = image_file[0] + "." + extension + image_file[1]
            output.save(output_file, image.format)
            os.chmod(output_file, mode)
    return 0


def main():
    '''If run from the command line, get command line option and arguments.'''
    from optparse import OptionParser

    logging.basicConfig(format="%(levelname)s: %(message)s")

    parser = OptionParser(usage="%prog [options] image1 [,image2...]")
    parser.set_defaults(overwrite=False, extension=None, color="alpha",
                        verbose=False)
    parser.add_option("-o", "--overwrite", action="store_true",
                      help="Overwrite all files.  Default is to not overwrite "+
                           "any files and instead generate new files with a "+
                           "'POT' extension.  This option cannot be combined "+
                           "with the 'extension' option.")
    parser.add_option("-e", "--extension", 
                      help="Set the extension added before the filetype.  The "+
                           "default is to add the 'pot' extension, ie. "+
                           "'image1.png' becomes 'image1.pot.png'.  This "+
                           "cannot be combined with the 'overwrite' option.")
    parser.add_option("-c", "--color", type="choice", 
                      choices=("alpha", "black", "white"),
                      help="Choose the padding color.  Default is 'alpha'.")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="Show extra information.")
    (opts, args) = parser.parse_args()

    if opts.verbose:
        logging.root.setLevel(logging.INFO)

    # ---Translate color string to RGBA tuple---
    assert opts.color.lower() in ("alpha", "black", "white")
    if opts.color.lower() == "alpha":
        color = (0,) * 4
    elif opts.color.lower() == "black":
        color = (0, 0, 0, 255)
    else:
        color = (255,) * 4

    # ---Decide between overwriting or adding an extension and run convert---
    if opts.overwrite and opts.extension:
        logging.error("You must specify ONLY an extension or overwrite.")
        parser.print_help()
        sys.exit(1)
    if not args:
        parser.print_usage()
        return 0
    if opts.overwrite:
        return convert(args, True, None, color)
    else:
        if opts.extension:
            if not isinstance(opts.extension, basestring):
                logging.error("'extension' must be a string.")
                parser.print_help()
                return 1
            return convert(args, False, opts.extension, color)
        else:
            return convert(args, False, "pot", color)
                      

if __name__ == "__main__":
    sys.exit(main())
