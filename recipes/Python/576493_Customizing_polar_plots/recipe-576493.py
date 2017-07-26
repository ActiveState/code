import pylab as m

m.polar(m.arange(360)*m.pi/180., m.rand(360))
m.thetagrids(angles, labels=None, fmt='%d', frac = 1.1)
m.rgrids(radii, labels=None, angle=22.5)
