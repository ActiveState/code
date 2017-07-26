#! /usr/bin/env python
import collections
import math
import random
import processing
import vector

################################################################################

# QVGA Resolution
WIDTH = 320
HEIGHT = 240

################################################################################

class Demo(processing.Process):

    "Demo.main(width, height) -> Starts the demonstration"

    NOT_CREATING_FISH = -1
    SCHOOLS = ('red', 'yellow'), ('blue', 'green')

    def setup(self, background):
        "Setup the screen and boids before starting simulation."
        background('black')
        self.schools = []
        self.sources = []
        for body_color, trim_color in self.SCHOOLS:
            new_school = School(body_color, trim_color)
            new_source = vector.Vector2(random.random() * WIDTH,
                                        random.random() * HEIGHT)
            self.schools.append(new_school)
            self.sources.append(new_source)
        self.pointer = 0

    def render(self, graphics):
        "Displays the boids on the graphics every time called."
        self.add_fish()
        graphics.clear()
        fish = 0
        for school in self.schools:
            school.render(graphics)
            fish += school.size()
        graphics.write(5, 5, fish, 'white')

    def add_fish(self):
        "Add a fish to the next school while creating more fish."
        if self.pointer != self.NOT_CREATING_FISH:
            new_fish = Fish(self.sources[self.pointer])
            self.schools[self.pointer].add_fish(new_fish)
            self.pointer = (self.pointer + 1) % len(self.SCHOOLS)

    def update(self, interval):
        "Run one step of the physics simulation for the interval."
        for school in self.schools:
            school.update(interval)

    def mouse_pressed(self, event):
        "Create fish at cursor and add to the smallest school."
        new_fish = Fish(vector.Vector2(event.x, event.y))
        min(self.schools, key=School.size).add_fish(new_fish)

    def speed_warning(self):
        "Stop creating fish and remove fish from largest school."
        self.pointer = self.NOT_CREATING_FISH
        max(self.schools, key=School.size).kill_fish()

################################################################################

class Fish:

    "Fish(location) -> Fish"

    HOW_WIDE = 6            # Width of the fish
    HOW_LONG = 12           # Length of the fish
    
    MAX_FORCE = 0.05        # Maximum directional steering force
    MAX_SPEED = 60.0        # Maximum speed at which to travel

    SEP_FACTOR = 1.5        # Arbitrary separation mutliplier
    ALI_FACTOR = 1.0        # Arbitrary alignment mutliplier
    COH_FACTOR = 1.0        # Arbitrary cohesion mutliplier
    
    DESIRED_SEPARATION = 7  # Turn from each other when closer
    NEIGHBOR_DISTANCE = 17  # Maximum distance for interactions

    ########################################################################

    # DO NOT CHANGE THE FOLLOWING SECTION
    
    limits = math.hypot(HOW_LONG, HOW_WIDE)
    radius = limits / 2

    DESIRED_SEPARATION += limits
    NEIGHBOR_DISTANCE += limits
    
    TOP = 0 - radius
    LEFT = 0 - radius
    RIGHT = WIDTH + radius
    BOTTOM = HEIGHT + radius
    
    SHAPE = processing.Polygon(vector.Vector2(HOW_LONG / +2, 0),
                               vector.Vector2(HOW_LONG / -2, HOW_WIDE / +2),
                               vector.Vector2(HOW_LONG / -2, HOW_WIDE / -2))
    
    del limits, radius, HOW_LONG, HOW_WIDE

    __slots__ = 'location', 'velocity', 'steering', 'body_color', 'trim_color'

    # END OF PRECALCULATED FISH VARIABLES

    ########################################################################

    def __init__(self, location):
        "Initialize the fish with several vectors and colors."
        self.location = location.copy()
        self.velocity = vector.Polar2(random.random() * self.MAX_SPEED,
                                      random.random() * 360)
        self.body_color = ''
        self.trim_color = ''

    def paint(self, body_color, trim_color):
        "Assign colors to the fish's body and trim (outline)."
        self.body_color = body_color
        self.trim_color = trim_color

    def render(self, graphics):
        "Draw the fish's shape on the given graphics context."
        polygon = self.SHAPE.copy()
        polygon.rotate(self.velocity.direction)
        polygon.translate(self.location)
        graphics.draw(polygon, self.body_color, self.trim_color)

    def run_AI(self, school):
        "Execute the three boid rules and store in steering."
        self.steering = vector.Vector2(0, 0)
        # Follow rules of separation, alignment, and cohesion.
        separation = vector.Vector2(0, 0)
        alignment = vector.Vector2(0, 0)
        cohesion = vector.Vector2(0, 0)
        # Track fish that are too close along with neighbours.
        too_close = False
        neighbors = 0
        # Loop over all other fish from the school fish is in.
        for fish in school:
            if fish is not self:
                # Get the difference in location and distance.
                offset = self.location - fish.location
                length = offset.magnitude
                # Find fish that are too close to current one.
                if length < self.DESIRED_SEPARATION:
                    separation += offset.normalize() / length
                    too_close = True
                # Try joining fish in fish's present vicinity.
                if length < self.NEIGHBOR_DISTANCE:
                    alignment += fish.velocity
                    cohesion += fish.location
                    neighbors += 1
        # Steer away from fish in this school that are nearby.
        if too_close:
            self.steering += self.correction(separation) * self.SEP_FACTOR
        # Gather with and align to schoolmates detected above.
        if neighbors:
            self.steering += self.correction(alignment) * self.ALI_FACTOR
            cohesion /= neighbors
            cohesion -= self.location
            self.steering += self.correction(cohesion) * self.ALI_FACTOR

    def correction(self, target):
        "Create a force towards the direction of the target."
        target.magnitude = self.MAX_SPEED
        return (target - self.velocity).limit(self.MAX_FORCE)

    def update(self, interval):
        "Change velocity and location with respect to time."
        self.velocity += self.steering / interval
        self.location += self.velocity.limit(self.MAX_SPEED) * interval
        self.wraparound()
    
    def wraparound(self):
        "Move the fish to wrap around the edges of the screen."
        if self.location.y < self.TOP:
            self.location.y = self.BOTTOM
        elif self.location.y > self.BOTTOM:
            self.location.y = self.TOP
        if self.location.x < self.LEFT:
            self.location.x = self.RIGHT
        elif self.location.x > self.RIGHT:
            self.location.x = self.LEFT

################################################################################

class School:

    "School(body_color, trim_color) -> School"

    __slots__ = 'body_color', 'trim_color', 'fish_deque'

    def __init__(self, body_color, trim_color):
        "Initialize school with color identity and fish container."
        self.body_color = body_color
        self.trim_color = trim_color
        self.fish_deque = collections.deque()

    def add_fish(self, fish):
        "Paint the fish with identity before adding to fish list."
        fish.paint(self.body_color, self.trim_color)
        self.fish_deque.append(fish)

    def remove_fish(self):
        "Take a fish from this school and return fish to caller."
        return self.fish_deque.popleft()

    def size(self):
        "Get number of fish in school and return the total count."
        return len(self.fish_deque)

    def render(self, graphics):
        "Draw each fish in this school to the graphics context."
        for fish in self.fish_deque:
            fish.render(graphics)

    def update(self, interval):
        "Run the AI code of each fish before updating positions."
        for fish in self.fish_deque:
            fish.run_AI(self.fish_deque)
        for fish in self.fish_deque:
            fish.update(interval)

    def kill_fish(self):
        "If there are any fish in this school, remove one of them."
        if self.size() > 0:
            self.remove_fish()

################################################################################

import recipe576904; recipe576904.bind_all(globals())
    
################################################################################

if __name__ == '__main__':
    Demo.main(WIDTH, HEIGHT)
