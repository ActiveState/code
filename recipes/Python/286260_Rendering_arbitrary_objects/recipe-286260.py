from twisted.application import internet
from twisted.application import service

from nevow import appserver
from nevow import compy
from nevow import inevow
from nevow import loaders
from nevow import rend
from nevow import tags as T


############################################################################
# Define some simple classes for out application data.

class Person:
    def __init__(self, firstName, lastName, nickname):
        self.firstName = firstName
        self.lastName = lastName
        self.nickname = nickname

class Bookmark:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class PersonView(compy.Adapter):
    """Render a full view of a Person.
    """
    __implements__ = inevow.IRenderer
    def rend(self, data):
        attrs = ['firstName', 'lastName', 'nickname']
        return T.div(_class="View person")[
            T.p['Person'],
            T.dl[
                [(T.dt[attr], T.dd[getattr(self.original, attr)])
                    for attr in attrs]
                ]
            ]

class BookmarkView(compy.Adapter):
    """Render a full view of a Bookmark.
    """
    __implements__ = inevow.IRenderer
    def rend(self, data):
        attrs = ['name', 'url']
        return T.div(_class="View bookmark")[
            T.p['Bookmark'],
            T.dl[
                [(T.dt[attr], T.dd[getattr(self.original, attr)])
                    for attr in attrs]
                ]
            ]
    

############################################################################
# Register the rendering adapters. Note, these could easily be defined in
# a text file and registered by name rather than class object.

compy.registerAdapter(PersonView, Person, inevow.IRenderer)
compy.registerAdapter(BookmarkView, Bookmark, inevow.IRenderer)

############################################################################
# Create some data for the application to do something with.

objs = [
    Person('Valetino', 'Volonghi', 'dialtone'),
    Person('Matt', 'Goodall', 'mg'),
    Bookmark('Nevow', 'http://www.nevow.com'),
    Person('Somebody', 'Else', 'Nevow2004'),
    Bookmark('Twisted', 'http://twistedmatrix.com/'),
    Bookmark('Python', 'http://www.python.org'),
    ]

############################################################################
# PSimple Page that renders objs list

class Page(rend.Page):

    def render_item(self, ctx, data):
        return inevow.IRenderer(data)

    docFactory = loaders.stan(
        T.html[
            T.body[
                T.ul(data=objs, render=rend.sequence)[
                T.li(pattern='item')[render_item]
                    ],
                ],
            ]
        )


############################################################################

application = service.Application('irenderer')
httpd = internet.TCPServer(8000, appserver.NevowSite(Page()))
httpd.setServiceParent(application)
