#==============================================================================
class Geometry(Canvas):
    
    def __init__(self, parent, **kwargs):
        # Tkinter doesn't support super(...) type initialisation
        Canvas.__init__(self, parent, kwargs)

    def draw_point(self, point, colour):
        self.create_oval(
            point[0] - 2,
            point[1] - 2,
            point[0] + 2,
            point[1] + 2,
            fill=colour,
            outline=""
            )

    def draw_circle(self, centre, radius, colour):
        # makes an oval, takes the top left coordinate and the bottom right
        self.create_oval(
            int(centre[0] - radius),
            int(centre[1] - radius),
            int(centre[0] + radius),
            int(centre[1] + radius),
            outline=colour,
            fill=""
            )
        # draw the centre
        self.draw_point(centre, colour)

    def draw_line(self, point, second_point, colour):
        self.create_line(
            point[0],
            point[1],
            second_point[0],
            second_point[1],
            fill=colour
            )
        
    def draw_polygon(self, points, colour):
        # tkinter wants the points like x0, y0, x1, y1, ... we give it as 
        # [(x0, y0), (x1, y1), ...]
        tkinter_compatible_points = list()
        for point in points:
            tkinter_compatible_points.append(point[0])
            tkinter_compatible_points.append(point[1])
        self.create_polygon(
            *tkinter_compatible_points,
             fill="",
             outline=colour
            )    
