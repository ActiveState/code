#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np

"""
This program is an extensible Conway's game of life. It allows to define
different type of grid (for example 2D or 3D) and more complex rules. 
Each grid inherits an Abstract grid that implement the method (next()) 
to pass for the next configuration. 
Furthermore, each element can be whatever type. In this
example I designed Grid2DBool that represent the simple Conway's game of life,
but could be possible to develop and easily implement more complex grids and
rules.

Note:
The demo save also the animation in a file .mp4 and plot it through pyplot.
The demo could take long time because of storing all the configurations before
showing the animation. Therefore, the visualization can be improved using other
libraries (as wxpython) that paint the configuration of the grid once it's
created.
With a more complex view it's convenient to apply MVC pattern declaring the
model AbstractGrid as the Observable class.

@author Filippo Squillace
@date 02/12/2011
@version 0.0.5
"""

class AbstractGrid():
    """
    This class represents the abstract grid that implement 
    the template method to generate the next configuration. The rules are
    definied in the abstract method next_state() and it's not
    implemented in this class because depends on the structure of the matrix
    and the type of elements in the grid.
    """
    def __init__(self):
        self.matrix = np.array([], dtype=bool)
    
    def __str__(self):
        return self.matrix.__str__()

    ####### Abstract methods ########
    def next_state(self, coords, el):
        raise NotImplementedError()
    def is_done(self):
        raise NotImplementedError()
    ################################

    def add_element(self, coords, el):
        self.matrix[coords] = el

    def next(self):
        # copy the matrix
        old_matrix = self.matrix.copy()
        itr = self.matrix.flat
        coords = itr.coords
        for el in itr:
            old_matrix[coords] = self.next_state(coords, el)
            coords = itr.coords

        # copy all the modifications
        self.matrix = old_matrix


class Grid2D(AbstractGrid):

    def __init__(self, n, m, typ=bool):
        AbstractGrid.__init__(self)
        self.n = n
        self.m = m
        self.matrix = np.array([None for x in range(n*m)], dtype=typ).reshape(n,m)

class Grid2DBool(Grid2D):
    """
    Represents the classical Conway's game of life with 2D grid 
    and each element can be either True (alive) or Fase (death)
    Params:
    n - number of rows
    m - number of columns
    """
    def __init__(self, n, m):
        Grid2D.__init__(self, n, m, bool)

    def add_element(self, x, y):
        t = (x, y)
        Grid2D.add_element(self, t, True)

    def next_state(self, coords, el):
        # Gets all information from the neighbors
        (x, y) = coords
        neighbors = 0
        if x==0:
            x1=0
        else:
            x1=x-1
        if x==self.n-1:
            x2=self.n-1
        else:
            x2=x+1

        if y==0:
            y1=0
        else:
            y1=y-1
        if y==self.m-1:
            y2=self.m-1
        else:
            y2=y+1

        for n in self.matrix[x1:x2+1, y1:y2+1].flat:
            if n:
                neighbors = neighbors + 1

        # Excludes the main element
        if el:
            neighbors = neighbors - 1
        
        if el: # el alives
            if neighbors==2 or neighbors==3:
                return True
            if neighbors<2 or neighbors>3:
                return False
        else: # el death
            if neighbors==3:
                return True
    
    def is_done(self):
        return not self.matrix.max() # there is no True


def light_spaceship(g, x, y, invert=False):
    """
    Puts the lightweight spaceship right in the grid starting from icoords
    """
    if not invert:
        g.add_element(x,y)
        g.add_element(x+2,y)
        g.add_element(x+3,y+1)
        g.add_element(x+3,y+2)
        g.add_element(x+3,y+3)
        g.add_element(x+3,y+4)
        g.add_element(x+2,y+4)
        g.add_element(x+1,y+4)
        g.add_element(x,y+3)
    else:
        g.add_element(x,y)
        g.add_element(x+2,y)
        g.add_element(x+3,y-1)
        g.add_element(x+3,y-2)
        g.add_element(x+3,y-3)
        g.add_element(x+3,y-4)
        g.add_element(x+2,y-4)
        g.add_element(x+1,y-4)
        g.add_element(x,y-3)


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    n = 50
    
    g = Grid2DBool(n, n)

    light_spaceship(g, 5,2)
    light_spaceship(g, 25,2)
    light_spaceship(g, 45,2)
    light_spaceship(g, 5,40, True)
    light_spaceship(g, 25,40, True)
    light_spaceship(g, 45,40, True)



    x = np.arange(0, n+1)
    y = np.arange(0, n+1)
    X,Y = np.meshgrid(x,y)
    ims = []
    ims.append((plt.pcolor(X, Y, g.matrix),))
    
    counter = 0
    while(not g.is_done() and counter < 100):
        g.next()
        ims.append((plt.pcolor(X, Y, g.matrix),))
        counter = counter + 1
    
    fig = plt.figure(1)
    im_ani = animation.ArtistAnimation(fig, ims, interval=2,\
            repeat_delay=3000,\
            blit=True)

    im_ani.save('im.mp4')
    plt.axis([0, n, n, 0])
    plt.axis('off')
    plt.show()
