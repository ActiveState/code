def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

def HTMLColorToPILColor(colorstring):
    """ converts #RRGGBB to PIL-compatible integers"""
    colorstring = colorstring.strip()
    while colorstring[0] == '#': colorstring = colorstring[1:]
    # get bytes in reverse order to deal with PIL quirk
    colorstring = colorstring[-2:] + colorstring[2:4] + colorstring[:2]
    # finally, make it numeric
    color = int(colorstring, 16)
    return color

def PILColorToRGB(pil_color):
    """ convert a PIL-compatible integer into an (r, g, b) tuple """
    hexstr = '%06x' % pil_color
    # reverse byte order
    r, g, b = hexstr[4:], hexstr[2:4], hexstr[:2]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

def PILColorToHTMLColor(pil_integer):
    return RGBToHTMLColor(PILColorToRGB(pil_integer))

def RGBToPILColor(rgb_tuple):
    return HTMLColorToPILColor(RGBToHTMLColor(rgb_tuple))

import Image
def getRGBTupleFromImg(file_obj, coords=(0,0)):
    """ 
    Extract an #RRGGBB color string from given pixel coordinates
    in the given file-like object.
    """
    pil_img = Image.open(file_obj)
    pil_img = pil_img.convert('RGB')
    rgb = pil_img.getpixel(coords)
    return rgb

if __name__ == '__main__':
    htmlcolor = '#ff00cc'
    pilcolor = HTMLColorToPILColor(htmlcolor)
    rgb = HTMLColorToRGB(htmlcolor)
    print pilcolor
    print htmlcolor
    print rgb
    print PILColorToHTMLColor(pilcolor)
    print PILColorToRGB(pilcolor)
    print RGBToPILColor(rgb)
    print RGBToHTMLColor(rgb)
    print
    img = open('/tmp/bkg.gif', 'r')
    print getRGBTupleFromImg(img, (0,0))
