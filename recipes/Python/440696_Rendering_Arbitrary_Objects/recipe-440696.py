import cherrypy

# here are our "arbitrary" object classes

class Person(object):
    def __init__(self, firstName, lastName, nickname):
        self.firstName = firstName
        self.lastName = lastName
        self.nickname = nickname

class Bookmark(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

# create a generic view

class GenericView(object):
    # subclasses should implement tmpl as string<--dict
    # substitution template
    tmpl = None
    
    def __init__(self, obj):
        self.obj = obj

    def render(self):
        return self.tmpl % self.obj.__dict__

# define our views

class PersonView(GenericView):
    "Define a person view"
    tmpl = """
    <div class="viewPerson">
        %(firstName)s %(lastName)s,
        <em>aka %(nickname)s</em>
    </div>"""

class BookmarkView(GenericView):
    "Define a bookmark view"
    tmpl = """
    <div class="bookmarkView">
        <a href="%(url)s">%(name)s</a>
    </div>"""

# here is our main application class

class ArbitraryObjects(object):
    header = "<html><head></head><body>"
    footer = "</body></html>"

    def __init__(self, handlers):
        self.handlers = handlers

    def map_view(self, obj):
        obj_class = obj.__class__
        return self.handlers[obj_class](obj)
    
    def index(self):
        yield self.header
        for item in objs:
            yield self.map_view(item).render()
        yield self.footer
    index.exposed = True

# now for some test data
objs = [
    Bookmark('TurboGears', 'http://www.turbogears.org'),
    Person('Robert', 'Brewer', 'fumanchu'),
    Person('Sylvain', 'Hellegouarch', 'Lawouach'),
    Bookmark('Subway', 'http://subway.python-hosting.com'),
    Bookmark('CherryPy', 'http://www.cherrypy.org'),
    Person('Remi', 'Delon', 'Remi'),
    ]


handlers = {
    Person:PersonView,
    Bookmark:BookmarkView
    }

# setup and start our application

cherrypy.root = ArbitraryObjects(handlers)

cherrypy.server.start()
