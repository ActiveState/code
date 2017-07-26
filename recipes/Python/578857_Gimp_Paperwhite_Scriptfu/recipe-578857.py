#!/usr/bin/env python

"""
paperwhite -- a gimp plugin (place me at ~/.gimp-2.6/plug-ins/ and give
              me execution permissions) for making fotographs of papers
              (documents) white in the background
"""

import math
from gimpfu import *

def python_paperwhite(timg, tdrawable, radius=12):
    layer = tdrawable.copy()
    timg.add_layer(layer)
    layer.mode = DIVIDE_MODE
    pdb.plug_in_despeckle(timg, layer, radius, 2, 7, 248)
    timg.flatten()
    pdb.gimp_levels(timg.layers[0], 0, 10, 230, 1.0, 0, 255)
    pdb.gimp_image_convert_indexed(timg,
        NO_DITHER, MAKE_PALETTE, 16, False, True, '')
    (bytesCount, colorMap) = pdb.gimp_image_get_colormap(timg)
    colormap = pdb.gimp_image_get_colormap(timg)[1]
    colors = [ colormap[i:i+3] for i in range(0, len(colormap), 3) ]
    enumeratedColors = list(enumerate(colors))
    indexOfLightest, lightest = max(enumeratedColors,
        key=lambda (n, (r, g, b)): r + g + b)
    indexOfDarkest, darkest = min(enumeratedColors,
        key=lambda (n, (r, g, b)): r + g + b)
    colors[indexOfLightest] = (255, 255, 255)
    colors[indexOfDarkest] = (0, 0, 0)
    colormap = sum(map(list, colors), [])
    pdb.gimp_image_set_colormap(timg, len(colormap), colormap)
    pdb.gimp_message("Consider saving as PNG now!")

register(
        "python_fu_paperwhite",
        "Make the paper of the photographed paper document white.",
        "Make the paper of the photographed paper document white.",
        "Alfe Berlin",
        "Alfe Berlin",
        "2012-2012",
        "<Image>/Filters/Artistic/Paperw_hite...",
        "RGB*, GRAY*",
        [
                (PF_INT, "radius", "Radius", 12),
        ],
        [],
        python_paperwhite)

main()
