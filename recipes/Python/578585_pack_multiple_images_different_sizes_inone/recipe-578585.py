#!/usr/bin/env python
"""
Pack multiple images of different sizes into one image.

Based on S W's recipe:
http://code.activestate.com/recipes/442299/
Licensed under the PSF License
"""
import argparse
import glob
import Image
import ImageChops

try: import timing # Optional, http://stackoverflow.com/a/1557906/724176
except: None

def tuple_arg(s):
    try:
        if ',' in s:
            w, h = map(int, s.split(','))
        elif ':' in s:
            w, h = map(int, s.split(':'))
        elif 'x' in s:
            w, h = map(int, s.split('x'))
        return w, h
    except:
        raise argparse.ArgumentTypeError("Value must be w,h or w:h or wxh")

class PackNode(object):
    """
    Creates an area which can recursively pack other areas of smaller sizes into itself.
    """
    def __init__(self, area):
        #if tuple contains two elements, assume they are width and height, and origin is (0,0)
        if len(area) == 2:
            area = (0,0,area[0],area[1])
        self.area = area

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.area))

    def get_width(self):
        return self.area[2] - self.area[0]
    width = property(fget=get_width)

    def get_height(self):
        return self.area[3] - self.area[1]
    height = property(fget=get_height)

    def insert(self, area):
        if hasattr(self, 'child'):
            a = self.child[0].insert(area)
            if a is None: 
                return self.child[1].insert(area)
            return a

        area = PackNode(area)
        if area.width <= self.width and area.height <= self.height:
            self.child = [None,None]
            self.child[0] = PackNode((self.area[0]+area.width, self.area[1], self.area[2], self.area[1] + area.height))
            self.child[1] = PackNode((self.area[0], self.area[1]+area.height, self.area[2], self.area[3]))
            return PackNode((self.area[0], self.area[1], self.area[0]+area.width, self.area[1]+area.height))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Pack multiple images of different sizes into one image.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--outfile', default='output.png',
        help='Output image file')
    parser.add_argument('-s', '--size', type=tuple_arg, metavar='pixels',
        help="Size (width,height tuple) of the image we're packing into", 
        default="1024,1024")
    parser.add_argument('-l', '--largest_first', action='store_true',
        help='Pack largest images first')
    parser.add_argument('-t', '--tempfiles', action='store_true',
        help='Save temporary files to show filling')
    args = parser.parse_args()
    print args

    format = 'RGBA'
    #get a list of PNG files in the current directory
    names = glob.glob("*.png")
    if args.outfile in names:
        names.remove(args.outfile) # don't include any pre-existing output

    #create a list of PIL Image objects, sorted by size
    print "Create a list of PIL Image objects, sorted by size"
    images = sorted([(i.size[0]*i.size[1], name, i) for name,i in ((x,Image.open(x).convert(format)) for x in names)], reverse=args.largest_first)

    print "Create tree"
    tree = PackNode(args.size)
    image = Image.new(format, args.size)

    #insert each image into the PackNode area
    for i, (area, name, img) in enumerate(images):
        print name, img.size
        uv = tree.insert(img.size)
        if uv is None: raise ValueError('Pack size ' + str(args.size) + ' too small, cannot insert ' + str(img.size) + ' image.')
        image.paste(img, uv.area)
        if args.tempfiles:
            image.save("temp" + str(i).zfill(4) + ".png")
 
    image.save(args.outfile)
    image.show()

# End of file
