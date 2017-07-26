import Image
import glob

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
            if a is None: return self.child[1].insert(area)
            return a

        area = PackNode(area)
        if area.width <= self.width and area.height <= self.height:
            self.child = [None,None]
            self.child[0] = PackNode((self.area[0]+area.width, self.area[1], self.area[2], self.area[1] + area.height))
            self.child[1] = PackNode((self.area[0], self.area[1]+area.height, self.area[2], self.area[3]))
            return PackNode((self.area[0], self.area[1], self.area[0]+area.width, self.area[1]+area.height))


if __name__ == "__main__":
    format = 'RGBA'
    #size of the image we are packing into
    size = 1024,1024
    #get a list of PNG files in the current directory
    names = glob.glob("*.png")
    #create a list of PIL Image objects, sorted by size
    images = sorted([(i.size[0]*i.size[1], name, i) for name,i in ((x,Image.open(x).convert(format)) for x in names)])

    tree = PackNode(size)
    image = Image.new(format, size)

    #insert each image into the PackNode area
    for area, name, img in images:
        uv = tree.insert(img.size)
        if uv is None: raise ValueError('Pack size too small.')
        image.paste(img, uv.area)

    image.show()
