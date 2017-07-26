"""
    @author   Thomas Lehmann
    @file     four_cubes_problem.py

    There are four cubes with concrete colors on their sides and the goal
    is to place each cube in one row that way, that along the row each side
    presents four different colors:

     -   -   -   -
    |W| |R| |G| |B| (front view)
     -   -   -   -

    Of course four different colors are also required at the top view
    at the bottom view and at the back view.

    Background: I have those four cubes in real and I have been seeking
                for the solution without manual try.

"""
import random

class Color:
    """ represents a kind of enum for all used colors """
    GREEN = 0
    RED   = 1
    WHITE = 2
    BLUE  = 3

    MAX   = 4

    @staticmethod
    def name(value):
        return ["GREEN", "RED", "WHITE", "BLUE"][value]

class Cube:
    def __init__(self, front, back, left, right, top, bottom):
        """ initializes all sides of a cube with colors """
        self.front  = front
        self.back   = back
        self.left   = left
        self.right  = right
        self.top    = top
        self.bottom = bottom

    def __eq__(self, other):
        """ compares this cube and another for to be equal """
        return self.front   == other.front  \
            and self.back   == other.back   \
            and self.left   == other.left   \
            and self.right  == other.right  \
            and self.top    == other.top    \
            and self.bottom == other.bottom

    def __hash__(self):
        """ unique key for this instance """
        return hash((self.front, self.back, self.left, self.right, self.top, self.bottom))

    def clone(self):
        """ provides a copy of this instance """
        return Cube(self.front, self.back, self.left, self.right, self.top, self.bottom)

    def __str__(self):
        """ does print the current cube setup (colors) """
        return "front:"  + Color.name(self.front)  + "," + \
               "back:"   + Color.name(self.back)   + "," + \
               "left:"   + Color.name(self.left)   + "," + \
               "right:"  + Color.name(self.right)  + "," + \
               "top:"    + Color.name(self.top)    + "," + \
               "bottom:" + Color.name(self.bottom)

    def getCombinations(self):
        """ I know: there should be 24 combinations """
        cubes = set()
        cubes.add(self.clone())

        cube = self.clone()
        while not len(cubes) == 24:
            mode = random.randint (0, 4)
            if   0 == mode:  cube.rotateLeft()
            elif 1 == mode:  cube.rotateRight()
            elif 2 == mode:  cube.rotateTop()
            elif 3 == mode:  cube.rotateBottom()
            cubes.add(cube.clone())

        return cubes

    def rotateLeft(self):
        """ does rotate the cube to the left """
        help       = self.left
        self.left  = self.front
        self.front = self.right
        self.right = self.back
        self.back  = help
        return self

    def rotateRight(self):
        """ does rotate the cube to the right """
        help       = self.right
        self.right = self.front
        self.front = self.left
        self.left  = self.back
        self.back  = help
        return self

    def rotateTop(self):
        """ does rotate the cube to the top """
        help        = self.top
        self.top    = self.front
        self.front  = self.bottom
        self.bottom = self.back
        self.back   = help
        return self

    def rotateBottom(self):
        """ does rotate the cube to the bottom """
        help        = self.bottom
        self.bottom = self.front
        self.front  = self.top
        self.top    = self.back
        self.back   = help
        return self

class CubesChecker:
    def __init__(self, cubes):
        self.originalCubes = cubes

    @staticmethod
    def isValidState(cubes):
        """ ensure the rule: four different colors on each side """
        frontColors  = set()
        backColors   = set()
        topColors    = set()
        bottomColors = set()

        for cube in cubes:
            frontColors.add(cube.front)
            backColors.add(cube.back)
            topColors.add(cube.top)
            bottomColors.add(cube.bottom)

        return  len(frontColors)  == Color.MAX \
            and len(backColors)   == Color.MAX \
            and len(topColors)    == Color.MAX \
            and len(bottomColors) == Color.MAX

    def calculate(self, position = 0, cubes = []):
        """ find the cubes final state """
        if len(cubes) == Color.MAX:
            if CubesChecker.isValidState(cubes):
                for cube in cubes:
                    print(cube)
                return True
            else:
                return False

        for cube in self.originalCubes[position].getCombinations():
            if self.calculate(position+1, cubes + [cube]):
                return True

        return False

def main():
    """ there are four cubes with concrete colors on their sides and the goal
        is to place each cube in one row that way that along the row each side
        presents four different colors """
    #              -----------  -----------  -----------  -----------  -----------  -----------
    #              front        back         left         right        top          bottom
    #              -----------  -----------  -----------  -----------  -----------  -----------
    cubes = [ Cube(Color.GREEN, Color.WHITE, Color.GREEN, Color.RED,   Color.WHITE, Color.BLUE),
              Cube(Color.WHITE, Color.RED  , Color.WHITE, Color.GREEN, Color.BLUE,  Color.RED),
              Cube(Color.RED,   Color.RED,   Color.RED  , Color.GREEN, Color.BLUE,  Color.WHITE),
              Cube(Color.BLUE,  Color.RED,   Color.GREEN, Color.GREEN, Color.WHITE, Color.BLUE) ]

    cubesChecker = CubesChecker(cubes)
    cubesChecker.calculate()

if __name__ == "__main__":
    main()
