import Image, ImageEnhance, os
from os.path import join

def test():
    batch("/media/disk/pics", "/home/hasanat/outputfolder/", "/home/hasanat/watermark.png")

def batch(infolder, outfolder, watermark):
    mark = Image.open(watermark)
    for root, dirs, files in os.walk(infolder):
        for name in files:        try:
            im = Image.open(join(root, name))
            if im.mode != 'RGBA':
                im = im.convert('RGBA')
            layer = Image.new('RGBA', im.size, (0,0,0,0))
            position = (im.size[0]-mark.size[0], im.size[1]-mark.size[1])
            layer.paste(mark, position)
            Image.composite(layer, im, layer).save( join(outfolder, name))
        except Exception, (msg):
            print msg

if __name__ == '__main__':
    test()
