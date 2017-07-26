## An extensible Conway's Game of Life  
Originally published: 2011-12-05 11:45:45  
Last updated: 2011-12-05 11:45:45  
Author: Filippo Squillace  
  
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