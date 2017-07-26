from tkinter import *
from random import randint, choice
from time import clock, sleep

# TODO: further tweaks
# 1. Add goals for the boids to move toward (DONE - BoidGroup.target)
# 2. Add wind or current that "blows" the boids around
# 3. Have boids tend towards a place; travel through waypoints
# 4. Limit (or unlimit) a boid's speed (DONE - BoidAgent.max_speed)
# 5. Set bounds for boids (DONE - BoidGUI.force_wall & .bounce_wall)
# 6. Allow boids to "perch" on the ground at random.

# TODO: anti-flocking behaviour
# 1. Get the boid group to scatter from each other; add more rules
# 2. Send the boids away from certain areas; danger or obstacles
# 3. Introduce predators that boids will always run from

# TODO: some other details
# 1. Boids need to "see" each other
# 2. Unseen boids should be ignored
# 3. Refer to the original algorithm
# 4. http://www.red3d.com/cwr/boids/
# 5. The timing engine needs redesign (DONE - based on pt.QT.run)
# 6. Change updating system to that used by QuizMe

################################################################################

# Here are various program settings.

USE_WINDOW = False  # Display program in window.
FULLSCREEN = True   # Go fullscreen when executed.

SCR_SAVER = False   # Turn screensaver mode on or off.
COME_BACK = -1      # The program can automatically "restart."
                    # if < 0: Exit program immediately
                    # if = 0: Disable exiting program
                    # if > 0: Come back after X seconds

TITLE = 'BOIDs'     # Title to show in windowed mode.
WIDTH = 800         # Width for window to display in.
HEIGHT = 600        # Height to display in window mode.

BACKGROUND = '#000' # Background color for the screen.
BOIDS = 10          # Number of boids to show in a group.

# BoidGUI and BoidAgent have settings too.

################################################################################

def main():
    # Create the opening window for the program.
    NoDefaultRoot()
    root = Tk()
    assert not (USE_WINDOW and FULLSCREEN), \
           'Only Window or Fullscreen may be used.'
    # Define the closing event handler.
    if COME_BACK < 0:
        def close(event=None):
            root.destroy()
    else:
        def close(event=None):
            if COME_BACK:
                root.withdraw()
                sleep(COME_BACK)
                for child in root.children.values():
                    if isinstance(child, BoidGUI):
                        child.last_time += COME_BACK
                root.deiconify()
    # Create window based on settings.
    if USE_WINDOW:
        root.resizable(False, False)
        root.title(TITLE)
        width = WIDTH
        height = HEIGHT
        position = ''
    elif FULLSCREEN:
        root.overrideredirect(True)
        if not SCR_SAVER:
            root.bind_all('<Escape>', close)
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        position = '+0+0'
    else:
        raise ValueError('Cannot determine window type to use.')
    # Configure the root window as needed.
    root.protocol('WM_DELETE_WINDOW', close)
    if SCR_SAVER:
        assert COME_BACK, 'Screen may not be locked as screensaver.'
        root.bind_all('<Motion>', close)
        root.bind_all('<Key>', close)
    root.geometry('{0}x{1}{2}'.format(width, height, position))
    # Create the application object that handles the GUI.
    app = BoidGUI(root, width, height, BACKGROUND, BOIDS)
    app.grid()
    root.mainloop()

################################################################################

# This function parses color strings.
def parse_color(string):
    assert len(string) == 7 and string[0] == '#', 'Not Color String!'
    number = []
    for index in range(1, len(string) - 1, 2):
        number.append(int(string[index:index+2], 16))
    return tuple(number)

# This function interpolates between two colors.
def interpolate(lower, upper, bias):
    A = 1 - bias
    R = round(lower[0] * A + upper[0] * bias)
    G = round(lower[1] * A + upper[1] * bias)
    B = round(lower[2] * A + upper[2] * bias)
    return R, G, B

################################################################################

class BoidGUI(Canvas):

    # Drawing Options
    BAL_NOT_VEC = True      # Draw balls (True) or vectors (False).
    RANDOM_BACK = False     # Replace background with flashing colors?
    RANDOM_BALL = False     # Replace balls with flashing colors?
    DRAW_TARGET = True      # Show line from groups to their targets?
    # Wall Settings
    WALL_BOUNCE = False     # Bouncy wall if true; force wall if false.
    WALL_MARGIN = 50        # Pixels from edge of screen for boundary.
    WALL_FORCE = 100        # Force applied to balls outside boundary.
    # Random Parameters
    MAX_FPS = 100           # Maximum frame per second for display.
    GROUPS = 2              # Number of groups to have displayed on the GUI.
    # Target Settings
    TARGET_FORCE = 500      # Force exerted by the targets on the boid groups.
    TRIG_DIST = 100         # Distance to target where target gets changed.
    MINI_DIST = 200         # Target must be this far away when recreated.
    # Boid Settings
    MAX_SPEED = 400         # Maximum speed for boids (pixels per second).
    MAX_SIZE = 15           # Largest radius a boid is allowed to have.
    MIN_SIZE = 10           # Smallest radius a boid may be built with.
    # Color Variables
    PALETTE_MODE = True     # Palette mode if true; random mode if false.
    COLORS = '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#FF00FF'
    PALETTE = []
    for x in range(16):
        for y in range(16):
            for z in range(16):
                color = '#{:X}{:X}{:X}'.format(x, y, z)
                PALETTE.append(color)
    # Check the settings up above for errors.
    assert MINI_DIST > TRIG_DIST, 'Targets must be set beyond trigger point.'
    assert MAX_SIZE > MIN_SIZE, 'A minimum may not be larger than maximum.'
    assert len(COLORS) > GROUPS, 'There must be more colors than groups.'

    def __init__(self, master, width, height, background, boids):
        # Initialize the Canvas object.
        cursor = 'none' if SCR_SAVER else ''
        super().__init__(master, width=width, height=height, cursor=cursor,
                         background=background, highlightthickness=0)
        self.width = width
        self.height = height
        self.background = background
        # Create colors for the balls.
        self.create_ball_palette(boids)
        # Build the boid control system.
        self.build_boids(boids)
        # Build loop for frame updating.
        self.last_time = clock()
        self.time_diff = 1 / self.MAX_FPS
        self.after(1000 // self.MAX_FPS, self.update_screen)

    def create_ball_palette(self, size):
        # The last color is not used.
        size += 1
        # Turn the colors into (R, G, B) tuples.
        colors = list(map(parse_color, self.COLORS))
        self.BALL_PALETTE = []
        for index in range(len(colors)):
            # Extract color bounds.
            lower = colors[index]
            upper = colors[(index + 1) % len(colors)]
            palette = []
            # Interpolate colors between the bounds.
            for bias in range(size):
                R, G, B = interpolate(lower, upper, bias / size)
                palette.append('#{0:02X}{1:02X}{2:02X}'.format(R, G, B))
            # Add the new palette to the choice list.
            self.BALL_PALETTE.append(palette)

    def build_boids(self, boids):
        # Build various boid simulation groups.
        self.groups = []
        for group in range(self.GROUPS):
            group = BoidGroup()
            group.palette = choice(self.BALL_PALETTE)
            self.BALL_PALETTE.remove(group.palette)
            # Create a new boid for current group.
            for boid, color in zip(range(boids), group.palette):
                # Place the boid somewhere on screen.
                x = randint(0, self.width)
                y = randint(0, self.height)
                position = Vector2(x, y)
                # Give it a random velocity (within 400).
                velocity = Polar2(randint(1, self.MAX_SPEED), randint(1, 360))
                # Create a random size for the ball.
                size = randint(self.MIN_SIZE, self.MAX_SIZE)
                assert size != 2, 'This is an oddly shaped ball.'
                # Create a boid (with a maximum speed of 400).
                boid = BoidAgent(position, velocity, size, self.MAX_SPEED)
                # Add a color attribute from COLORS list.
                if self.PALETTE_MODE:
                    boid.color = color
                else:
                    boid.color = choice(self.COLORS)
                group.add_boid(boid)
            # Add some mutators to this group.
            if self.WALL_BOUNCE:
                group.add_control(self.bounce_wall)
            else:
                group.add_control(self.force_wall)
            group.add_control(self.motivate)
            # Add a random target attribute to the group.
            x = randint(self.WALL_MARGIN, self.width - self.WALL_MARGIN)
            y = randint(self.WALL_MARGIN, self.height - self.WALL_MARGIN)
            group.target = Vector2(x, y)
            self.groups.append(group)

    def motivate(self, group, boid, seconds):
        # What direction should this boid move in?
        vector = (group.target - boid.position).unit()
        # Adjust velocity according to force and scale.
        boid.velocity += vector * self.TARGET_FORCE * seconds

    def check_target(self):
        for group in self.groups:
            # Is the center of the group within (100) pixels of target?
            if (group.center - group.target).magnitude <= self.TRIG_DIST:
                # Adjust target to be over (200) pixels away.
                while (group.center - group.target).magnitude <= self.MINI_DIST:
                    minimum = self.WALL_MARGIN
                    width = self.width - minimum
                    height = self.height - minimum
                    x = randint(minimum, width)
                    y = randint(minimum, height)
                    group.target = Vector2(x, y)
                # Change the ball colors if they are not random.
                if not self.RANDOM_BALL:
                    if self.PALETTE_MODE:
                        palette = choice(self.BALL_PALETTE)
                        self.BALL_PALETTE.remove(palette)
                        self.BALL_PALETTE.append(group.palette)
                        # Assign colors from new palette.
                        for boid, color in zip(group.boids, palette):
                            boid.color = color
                        group.palette = palette
                    else:
                        # Assign a random color from palette.
                        for boid in group.boids:
                            boid.color = choice(self.COLORS)
                    

    def force_wall(self, group, boid, seconds):
        # Left and Right walls.
        if boid.position.x < self.WALL_MARGIN:
            boid.velocity.x += self.WALL_FORCE * seconds
        elif boid.position.x > self.width - self.WALL_FORCE:
            boid.velocity.x -= self.WALL_FORCE * seconds
        # Upper and Lower walls.
        if boid.position.y < self.WALL_MARGIN:
            boid.velocity.y += self.WALL_FORCE * seconds
        elif boid.position.y > self.height - self.WALL_FORCE:
            boid.velocity.y -= self.WALL_FORCE * seconds

    def bounce_wall(self, group, boid, seconds):
        # Left and Right walls.
        if boid.position.x < self.WALL_MARGIN:
            if boid.velocity.x < 0:
                boid.velocity.x *= -1
        elif boid.position.x > self.width - self.WALL_MARGIN:
            if boid.velocity.x > 0:
                boid.velocity.x *= -1
        # Upper and Lower walls.
        if boid.position.y < self.WALL_MARGIN:
            if boid.velocity.y < 0:
                boid.velocity.y *= -1
        elif boid.position.y > self.height - self.WALL_MARGIN:
            if boid.velocity.y > 0:
                boid.velocity.y *= -1

    def update_screen(self):
        # Clear the screen.
        self.delete(ALL)
        for group in self.groups:
            # Draw the group's target if enabled.
            if self.DRAW_TARGET:
                center = group.center
                target = group.target
                self.create_line(center.x, center.y, target.x, target.y,
                                 fill=choice(self.PALETTE), width=3)
            # Draw all boids in the current group.
            for boid in group.boids:
                # Select correct fill color for drawing.
                fill = choice(self.PALETTE) if self.RANDOM_BALL else boid.color
                if self.BAL_NOT_VEC:
                    # Draw a ball (oval).
                    x1 = boid.position.x - boid.radius
                    y1 = boid.position.y - boid.radius
                    x2 = boid.position.x + boid.radius
                    y2 = boid.position.y + boid.radius
                    self.create_oval((x1, y1, x2, y2), fill=fill)
                else:
                    # Draw a direction pointer.
                    start = boid.position
                    end = boid.velocity.unit() * (boid.radius * 3) + start
                    self.create_line(start.x, start.y, end.x, end.y,
                                     fill=fill, width=3)
        # Randomize the background color if enabled.
        if self.RANDOM_BACK:
            self['background'] = choice(self.PALETTE)
        # Update all group targets as needed.
        self.check_target()
        # Run through the updating routines on the groups.
        time = clock()
        delta = time - self.last_time
        for group in self.groups:
            group.run_controls(delta)
            group.update_velocity()
            group.update_position(delta)
        self.last_time = time
        # Schedule for the next run of this method.
        plus = time + self.time_diff
        over = plus % self.time_diff
        diff = plus - time - over
        self.after(round(diff * 1000), self.update_screen)

import _tkinter # Properly set the GUI's update rate.
_tkinter.setbusywaitinterval(1000 // BoidGUI.MAX_FPS)

################################################################################

# This is where groups and world objects should live.
class BoidWorld:
    pass

################################################################################

class BoidGroup:

    # Simple collection for managing boid agents.

    def __init__(self):
        self.__boids = []
        self.__flag = False
        self.__controls = []
        self.__good_center = False
        self.__prop_center = Vector2(0, 0)
        self.__good_vector = False
        self.__prop_vector = Vector2(0, 0)

    def add_boid(self, boid):
        self.__boids.append(boid)

    def update_velocity(self):
        assert not self.__flag, 'Position must be updated first.'
        self.__flag = True
        for boid in self.__boids:
            boid.update_velocity(self, self.__boids)
        self.__good_vector = False

    def update_position(self, seconds):
        assert self.__flag, 'Velocity must be updated first.'
        self.__flag = False
        for boid in self.__boids:
            boid.update_position(seconds)
        self.__good_center = False

    def add_control(self, control):
        self.__controls.append(control)

    def run_controls(self, seconds):
        for control in self.__controls:
            for boid in self.__boids:
                control(self, boid, seconds)

    @property
    def boids(self):
        for boid in self.__boids:
            yield boid

    @property
    def center(self):
        if self.__good_center == False:
            self.__prop_center = Vector2(0, 0)
            for boid in self.__boids:
                self.__prop_center += boid.position
            self.__prop_center /= len(self.__boids)
            self.__good_center = True
        return self.__prop_center

    @property
    def vector(self):
        if self.__good_vector == False:
            self.__prop_vector = Vector2(0, 0)
            for boid in self.__boids:
                self.__prop_vector += boid.velocity
            self.__prop_vector /= len(self.__boids)
            self.__good_vector = True
        return self.__prop_vector

################################################################################

class BoidAgent:

    # Implements all three boid rules.

    RULE_1_SCALE = 100  # Scale the clumping factor.
    RULE_2_SCALE = 3    # Scale the avoiding factor.
    RULE_2_SPACE = 1    # Avoid when inside of space.
    RULE_3_SCALE = 100  # Scale the schooling factor.

    def __init__(self, position, velocity, radius, max_speed):
        self.position = position
        self.velocity = velocity
        self.__update = Vector2(0, 0)
        self.radius = radius
        self.max_speed = max_speed

    def update_velocity(self, group, boids):
        # Filter self out of boids.
        others = [boid for boid in boids if boid is not self]
        # Run through the boid rules.
        vector_1 = self.__rule_1(others)
        # vector_1 = (group.center - self.position) / 100
        vector_2 = self.__rule_2(others)
        vector_3 = self.__rule_3(others)
        # vector_3 = (group.vector - self.velocity) / 100
        # Save the results.
        self.__update = vector_1 + vector_2 + vector_3

    def update_position(self, seconds):
        # Update to new velocity.
        self.velocity += self.__update
        # Limit the velocity as needed.
        if self.velocity.magnitude > self.max_speed:
            self.velocity /= self.velocity.magnitude / self.max_speed
        # Update our position variable.
        self.position += self.velocity * seconds

    def __rule_1(self, boids):
        # Simulate the clumping factor.
        vector = Vector2(0, 0)
        for boid in boids:
            vector += boid.position
        vector /= len(boids)
        return (vector - self.position) / self.RULE_1_SCALE

    def __rule_2(self, boids):
        # Simulate the avoiding factor.
        vector = Vector2(0, 0)
        for boid in boids:
            delta = (boid.position - self.position).magnitude
            space = (boid.radius + self.radius) * (self.RULE_2_SPACE + 1)
            if delta < space:
                vector += (self.position - boid.position)
        return vector / self.RULE_2_SCALE

    def __rule_3(self, boids):
        # Simulate the schooling factor.
        vector = Vector2(0, 0)
        weight = 0
        for boid in boids:
            r2 = boid.radius ** 2
            vector += boid.velocity * r2
            weight += r2
        vector /= len(boids) * weight
        return (vector - self.velocity) / self.RULE_3_SCALE

################################################################################

from math import *

################################################################################

def Polar2(magnitude, degrees):
    x = magnitude * sin(radians(degrees))
    y = magnitude * cos(radians(degrees))
    return Vector2(x, y)

################################################################################

class Vector2:

    # See all the nice vector operations above?
    # The following class implements those instructions.

    __slots__ = 'x', 'y'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector2({!r}, {!r})'.format(self.x, self.y)

    def polar_repr(self):
        x, y = self.x, self.y
        magnitude = hypot(x, y)
        angle = degrees(atan2(x, y)) % 360
        return 'Polar2({!r}, {!r})'.format(magnitude, angle)

    # Rich Comparison Methods

    def __lt__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 < x2 * x2 + y2 * y2
        return hypot(self.x, self.y) < obj

    def __le__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 <= x2 * x2 + y2 * y2
        return hypot(self.x, self.y) <= obj

    def __eq__(self, obj):
        if isinstance(obj, Vector2):
            return self.x == obj.x and self.y == obj.y
        return hypot(self.x, self.y) == obj

    def __ne__(self, obj):
        if isinstance(obj, Vector2):
            return self.x != obj.x or self.y != obj.y
        return hypot(self.x, self.y) != obj

    def __gt__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 > x2 * x2 + y2 * y2
        return hypot(self.x, self.y) > obj

    def __ge__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 >= x2 * x2 + y2 * y2
        return hypot(self.x, self.y) >= obj

    # Boolean Operation

    def __bool__(self):
        return self.x != 0 or self.y != 0

    # Container Methods

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __setitem__(self, index, value):
        temp = [self.x, self.y]
        temp[index] = value
        self.x, self.y = temp

    def __iter__(self):
        yield self.x
        yield self.y

    def __reversed__(self):
        yield self.y
        yield self.x

    def __contains__(self, obj):
        return obj in (self.x, self.y)

    # Binary Arithmetic Operations

    def __add__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x + obj.x, self.y + obj.y)
        return Vector2(self.x + obj, self.y + obj)

    def __sub__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x - obj.x, self.y - obj.y)
        return Vector2(self.x - obj, self.y - obj)

    def __mul__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x * obj.x, self.y * obj.y)
        return Vector2(self.x * obj, self.y * obj)

    def __truediv__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x / obj.x, self.y / obj.y)
        return Vector2(self.x / obj, self.y / obj)

    def __floordiv__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x // obj.x, self.y // obj.y)
        return Vector2(self.x // obj, self.y // obj)

    def __mod__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x % obj.x, self.y % obj.y)
        return Vector2(self.x % obj, self.y % obj)

    def __divmod__(self, obj):
        if isinstance(obj, Vector2):
            return (Vector2(self.x // obj.x, self.y // obj.y),
                    Vector2(self.x % obj.x, self.y % obj.y))
        return (Vector2(self.x // obj, self.y // obj),
                Vector2(self.x % obj, self.y % obj))

    def __pow__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x ** obj.x, self.y ** obj.y)
        return Vector2(self.x ** obj, self.y ** obj)

    def __lshift__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x << obj.x, self.y << obj.y)
        return Vector2(self.x << obj, self.y << obj)

    def __rshift__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x >> obj.x, self.y >> obj.y)
        return Vector2(self.x >> obj, self.y >> obj)

    def __and__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x & obj.x, self.y & obj.y)
        return Vector2(self.x & obj, self.y & obj)

    def __xor__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x ^ obj.x, self.y ^ obj.y)
        return Vector2(self.x ^ obj, self.y ^ obj)

    def __or__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x | obj.x, self.y | obj.y)
        return Vector2(self.x | obj, self.y | obj)

    # Binary Arithmetic Operations (with reflected operands)

    def __radd__(self, obj):
        return Vector2(obj + self.x, obj + self.y)

    def __rsub__(self, obj):
        return Vector2(obj - self.x, obj - self.y)

    def __rmul__(self, obj):
        return Vector2(obj * self.x, obj * self.y)

    def __rtruediv__(self, obj):
        return Vector2(obj / self.x, obj / self.y)

    def __rfloordiv__(self, obj):
        return Vector2(obj // self.x, obj // self.y)

    def __rmod__(self, obj):
        return Vector2(obj % self.x, obj % self.y)

    def __rdivmod__(self, obj):
        return (Vector2(obj // self.x, obj // self.y),
                Vector2(obj % self.x, obj % self.y))

    def __rpow__(self, obj):
        return Vector2(obj ** self.x, obj ** self.y)

    def __rlshift__(self, obj):
        return Vector2(obj << self.x, obj << self.y)

    def __rrshift__(self, obj):
        return Vector2(obj >> self.x, obj >> self.y)

    def __rand__(self, obj):
        return Vector2(obj & self.x, obj & self.y)

    def __rxor__(self, obj):
        return Vector2(obj ^ self.x, obj ^ self.y)

    def __ror__(self, obj):
        return Vector2(obj | self.x, obj | self.y)

    # Augmented Arithmetic Assignments

    def __iadd__(self, obj):
        if isinstance(obj, Vector2):
            self.x += obj.x
            self.y += obj.y
        else:
            self.x += obj
            self.y += obj
        return self

    def __isub__(self, obj):
        if isinstance(obj, Vector2):
            self.x -= obj.x
            self.y -= obj.y
        else:
            self.x -= obj
            self.y -= obj
        return self

    def __imul__(self, obj):
        if isinstance(obj, Vector2):
            self.x *= obj.x
            self.y *= obj.y
        else:
            self.x *= obj
            self.y *= obj
        return self

    def __itruediv__(self, obj):
        if isinstance(obj, Vector2):
            self.x /= obj.x
            self.y /= obj.y
        else:
            self.x /= obj
            self.y /= obj
        return self

    def __ifloordiv__(self, obj):
        if isinstance(obj, Vector2):
            self.x //= obj.x
            self.y //= obj.y
        else:
            self.x //= obj
            self.y //= obj
        return self

    def __imod__(self, obj):
        if isinstance(obj, Vector2):
            self.x %= obj.x
            self.y %= obj.y
        else:
            self.x %= obj
            self.y %= obj
        return self

    def __ipow__(self, obj):        
        if isinstance(obj, Vector2):
            self.x **= obj.x
            self.y **= obj.y
        else:
            self.x **= obj
            self.y **= obj
        return self

    def __ilshift__(self, obj):
        if isinstance(obj, Vector2):
            self.x <<= obj.x
            self.y <<= obj.y
        else:
            self.x <<= obj
            self.y <<= obj
        return self

    def __irshift__(self, obj):
        if isinstance(obj, Vector2):
            self.x >>= obj.x
            self.y >>= obj.y
        else:
            self.x >>= obj
            self.y >>= obj
        return self

    def __iand__(self, obj):
        if isinstance(obj, Vector2):
            self.x &= obj.x
            self.y &= obj.y
        else:
            self.x &= obj
            self.y &= obj
        return self

    def __ixor__(self, obj):
        if isinstance(obj, Vector2):
            self.x ^= obj.x
            self.y ^= obj.y
        else:
            self.x ^= obj
            self.y ^= obj
        return self

    def __ior__(self, obj):
        if isinstance(obj, Vector2):
            self.x |= obj.x
            self.y |= obj.y
        else:
            self.x |= obj
            self.y |= obj
        return self

    # Unary Arithmetic Operations

    def __pos__(self):
        return Vector2(+self.x, +self.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __invert__(self):
        return Vector2(~self.x, ~self.y)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    # Virtual "magnitude" Attribute
    
    def __fg_ma(self):
        return hypot(self.x, self.y)

    def __fs_ma(self, value):
        x, y = self.x, self.y
        temp = value / hypot(x, y)
        self.x, self.y = x * temp, y * temp

    magnitude = property(__fg_ma, __fs_ma, doc='Virtual "magnitude" Attribute')

    # Virtual "direction" Attribute
    
    def __fg_di(self):
        return atan2(self.y, self.x)

    def __fs_di(self, value):
        temp = hypot(self.x, self.y)
        self.x, self.y = cos(value) * temp, sin(value) * temp

    direction = property(__fg_di, __fs_di, doc='Virtual "direction" Attribute')

    # Virtual "degrees" Attribute
    
    def __fg_de(self):
        return degrees(atan2(self.x, self.y)) % 360

    def __fs_de(self, value):
        temp = hypot(self.x, self.y)
        self.x, self.y = sin(radians(value)) * temp, cos(radians(value)) * temp

    degrees = property(__fg_de, __fs_de, doc='Virtual "degrees" Attribute')

    # Virtual "xy" Attribute

    def __fg_xy(self):
        return self.x, self.y

    def __fs_xy(self, value):
        self.x, self.y = value

    xy = property(__fg_xy, __fs_xy, doc='Virtual "xy" Attribute')

    # Virtual "yx" Attribute

    def __fg_yx(self):
        return self.y, self.x

    def __fs_yx(self, value):
        self.y, self.x = value

    yx = property(__fg_yx, __fs_yx, doc='Virtual "yx" Attribute')

    # Unit Vector Operations

    def unit_vector(self):
        x, y = self.x, self.y
        temp = hypot(x, y)
        return Vector2(x / temp, y / temp)

    def normalize(self):
        x, y = self.x, self.y
        temp = hypot(x, y)
        self.x, self.y = x / temp, y / temp
        return self

    # Vector Multiplication Operations

    def dot_product(self, vec):
        return self.x * vec.x + self.y * vec.y

    def cross_product(self, vec):
        return self.x * vec.y - self.y * vec.x

    # Geometric And Physical Reflections

    def reflect(self, vec):
        x1, y1, x2, y2 = self.x, self.y, vec.x, vec.y
        temp = 2 * (x1 * x2 + y1 * y2) / (x2 * x2 + y2 * y2)
        return Vector2(x2 * temp - x1, y2 * temp - y1)

    def bounce(self, vec):
        x1, y1, x2, y2 = self.x, self.y, +vec.y, -vec.x
        temp = 2 * (x1 * x2 + y1 * y2) / (x2 * x2 + y2 * y2)
        return Vector2(x2 * temp - x1, y2 * temp - y1)

    # Standard Vector Operations

    def project(self, vec):
        x, y = vec.x, vec.y
        temp = (self.x * x + self.y * y) / (x * x + y * y)
        return Vector2(x * temp, y * temp)

    def rotate(self, vec):
        x1, y1, x2, y2 = self.x, self.y, vec.x, vec.y
        return Vector2(x1 * x2 + y1 * y2, y1 * x2 - x1 * y2)

    def interpolate(self, vec, bias):
        a = 1 - bias
        return Vector2(self.x * a + vec.x * bias, self.y * a + vec.y * bias)

    # Other Useful Methods

    def near(self, vec, dist):
        x, y = self.x, self.y
        return x * x + y * y <= dist * dist

    def perpendicular(self):
        return Vector2(+self.y, -self.x)

    def subset(self, vec1, vec2):
        x1, x2 = vec1.x, vec2.x
        if x1 <= x2:
            if x1 <= self.x <= x2:
                y1, y2 = vec1.y, vec2.y
                if y1 <= y2:
                    return y1 <= self.y <= y2
                return y2 <= self.y <= y1
        else:
            if x2 <= self.x <= x1:
                y1, y2 = vec1.y, vec2.y
                if y1 <= y2:
                    return y1 <= self.y <= y2
                return y2 <= self.y <= y1
        return False

    # Synonymous Definitions

    copy = __pos__

    inverse = __neg__

    unit = unit_vector

    dot = dot_product

    cross = cross_product

    lerp = interpolate

    perp = perpendicular

################################################################################

# If this code is run directly,
# run the program's entry point.
if __name__ == '__main__':
    main()
