#!/usr/bin/env python3

'''Simple function to define a map with North/South Polar Stereographic
projection focused in a region of the globe (Basemap object).

When plotting maps with either 'npstere' or 'spstere' projections with the
Basemap toolkit for Matplotlib, the pole will always be placed in the center of
the figure. With this function you can zoom the map to the area of interest by
giving the latitude/longitudes coordinates of the bounds.

'''

import math

import mpl_toolkits.basemap as basemap
#import pyproj


def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
    '''Returns a Basemap object (NPS/SPS) focused in a region.

    lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
                                  W and S directions are negative.
    **kwargs -- Aditional arguments for Basemap object.

    '''
    lon_0 = lon_w + (lon_e - lon_w) / 2.
    ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
    lat_0 = math.copysign(90., ref)
    proj = 'npstere' if lat_0 > 0 else 'spstere'
    prj = basemap.Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='c')
    #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
    lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
    lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
    x, y = prj(lons, lats)
    ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
    ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
    return basemap.Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                           llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                           urcrnrlon=ur_lon, urcrnrlat=ur_lat, **kwargs)


# -----------------------------------------------------------------------------

# TESTING THE FUNCTION

import numpy as np
import matplotlib.pyplot as plt


def draw_latlon_polygon(bmap, lons, lats, *args, **kwargs):
    '''Plot a polygon in lat/lon coordinates.

    bmap -- Basemap object.
    lons, lats -- Sequences of polygon vertices.
    *args, **kwargs -- Aditional arguments to pyplot.plot().

    You should use 'k-' in *args to draw the lines in color black.

    '''
    if len(lons) != len(lats):
        raise IndexError('lons and lats have different lenghts')
    if lons[-1] != lons[0] or lats[-1] != lats[0]:
        lons = np.concatenate((lons, lons[:1]))
        lats = np.concatenate((lats, lats[:1]))
    n = len(lons) - 1
    res = 10000
    for i in range(n):
        x = np.linspace(lons[i], lons[i + 1], res)
        y = np.linspace(lats[i], lats[i + 1], res)
        x, y = bmap(x, y)
        bmap.plot(x, y, *args, **kwargs)


if __name__ == '__main__':
    nps = polar_stere(-10, 40, 30, 75, resolution='l')
    nps.drawmapboundary(fill_color='AntiqueWhite')
    nps.fillcontinents(color='BurlyWood', lake_color='AntiqueWhite')
    mer = np.arange(-60, 120, 10.)
    par = np.arange(0, 90, 10.)
    nps.drawparallels(par, linewidth=0.5, dashes=[1, 5])
    nps.drawmeridians(mer, linewidth=0.5, dashes=[1, 5])
    draw_latlon_polygon(nps, [-10, -10, 40, 40], [30, 75, 75, 30], 'k-')
    plt.title('NPS focused in lon=[10W, 40E] and lat=[30N, 75N]\nThis region is enclosed with black line')
    plt.show()
