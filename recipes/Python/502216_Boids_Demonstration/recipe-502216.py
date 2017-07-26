import random           # FOR RANDOM BEGINNINGS
from Tkinter import *   # ALL VISUAL EQUIPMENT

WIDTH = 800             # OF SCREEN IN PIXELS
HEIGHT = 600            # OF SCREEN IN PIXELS
BOIDS = 20              # IN SIMULATION
WALL = 100              # FROM SIDE IN PIXELS
WALL_FORCE = 10         # ACCELERATION PER MOVE
SPEED_LIMIT = 500       # FOR BOID VELOCITY
BOID_RADIUS = 3         # FOR BOIDS IN PIXELS
OFFSET_START = 20       # FROM WALL IN PIXELS

################################################################################

def main():
    # Start the program.
    initialise()
    mainloop()

def initialise():
    # Setup simulation variables.
    build_boids()
    build_graph()

def build_graph():
    # Build GUI environment.
    global graph
    root = Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth() - WIDTH) / 2, (root.winfo_screenheight() - HEIGHT) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.after(40, update)
    graph.pack()

def update():
    # Main simulation loop.
    draw()
    move()
    graph.after(40, update)

def draw():
    # Draw all boids.
    graph.delete(ALL)
    for boid in boids:
        x1 = boid.position.x - BOID_RADIUS
        y1 = boid.position.y - BOID_RADIUS
        x2 = boid.position.x + BOID_RADIUS
        y2 = boid.position.y + BOID_RADIUS
        
        graph.create_oval((x1, y1, x2, y2), fill='red')
    graph.update()

def move():
    # Move all boids.
    for boid in boids:
        simulate_wall(boid)
    for boid in boids:
        boid.update_velocity(boids)
    for boid in boids:
        boid.move()

def simulate_wall(boid):
    # Create viewing boundaries.
    if boid.position.x < WALL:
        boid.velocity.x += WALL_FORCE
    elif boid.position.x > WIDTH - WALL:
        boid.velocity.x -= WALL_FORCE
    if boid.position.y < WALL:
        boid.velocity.y += WALL_FORCE
    elif boid.position.y > HEIGHT - WALL:
        boid.velocity.y -= WALL_FORCE

def limit_speed(boid):
    # Limit boid speed.
    if boid.velocity.mag() > SPEED_LIMIT:
        boid.velocity /= boid.velocity.mag() / SPEED_LIMIT

def build_boids():
    # Create boids variable.
    global boids
    boids = tuple(Boid(WIDTH, HEIGHT, OFFSET_START) for boid in xrange(BOIDS))

################################################################################

# TWO DIMENTIONAL VECTOR CLASS

class TwoD:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return 'TwoD(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        return TwoD(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return TwoD(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return TwoD(self.x * other, self.y * other)

    def __div__(self, other):
        return TwoD(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __idiv__(self, other):
        if isinstance(other, TwoD):
            self.x /= other.x if other.x else 1
            self.y /= other.y if other.y else 1
        else:
            self.x /= other
            self.y /= other
        return self

    def mag(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

################################################################################

# BOID RULE IMPLEMENTATION CLASS

class Boid:

    def __init__(self, width, height, offset):
        self.velocity = TwoD(0, 0)
        self.position = TwoD(*self.random_start(width, height, offset))

    def random_start(self, width, height, offset):
        if random.randint(0, 1):
            # along left and right
            y = random.randint(1, height)
            if random.randint(0, 1):
                # along left
                x = -offset
            else:
                # along right
                x = width + offset
        else:
            # along top and bottom
            x = random.randint(1, width)
            if random.randint(0, 1):
                # along top
                y = -offset
            else:
                # along bottom
                y = height + offset
        return x, y


    def update_velocity(self, boids):
        v1 = self.rule1(boids)
        v2 = self.rule2(boids)
        v3 = self.rule2(boids)
        self.__temp = v1 + v2 + v3

    def move(self):
        self.velocity += self.__temp
        limit_speed(self)
        self.position += self.velocity / 100

    def rule1(self, boids):
        # clumping
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                vector += boid.position
        vector /= len(boids) - 1
        return (vector - self.position) / 7.5

    def rule2(self, boids):
        # avoidance
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                if (self.position - boid.position).mag() < 25:
                    vector -= (boid.position - self.position)
        return vector

    def rule3(self, boids):
        # schooling
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                vector += boid.velocity
        vector /= len(boids) - 1
        return (vector - self.velocity) / 2

################################################################################

# Execute the simulation.
if __name__ == '__main__':
    main()
