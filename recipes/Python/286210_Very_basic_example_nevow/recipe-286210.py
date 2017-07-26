from twisted.application import service, internet

from nevow import rend, loaders, appserver

class Pg(rend.Page):
    docFactory = loaders.htmlstr("""
    <html><head><title>Nested Maps Sequence Rendering</title></head>
        <body>
            <ul nevow:data="dct" nevow:render="sequence">
                <li nevow:pattern="item" nevow:render="mapping">
                    <span><nevow:slot name="name">Name</nevow:slot></span>
                    <span><nevow:slot name="surname">Surname</nevow:slot></span>
                    <span><nevow:slot name="age">Age</nevow:slot></span>
                </li>
            </ul>
        </body>
    </html>
    """)
    def __init__(self, dct):
        self.data_dct = dct
        rend.Page.__init__(self)

dct = [{'name':'Mark',
            'surname':'White',
            'age':'45'},
          {'name':'Valentino',
            'surname':'Volonghi',
            'age':'21'},
           {'name':'Peter',
             'surname':'Parker',
             'age':'Unknown'}
        ]

site = appserver.NevowSite(
    Pg(dct)
)
 
application = service.Application("example")
internet.TCPServer(8080, site).setServiceParent(application)

####
#### Using stan
####

from nevow import tags as T
from nevow import rend, loaders, appserver
from twisted.application import service, internet

class Pg(rend.Page):
    docFactory = loaders.stan(
        T.html[T.head[T.title["Nested Maps Sequence Rendering"]],
            T.body[
                T.ul(data=T.directive("dct"), render=T.directive("sequence"))[
                    T.li(pattern="item", render=T.directive("mapping"))[
                        T.span[T.slot("name")],
                        T.span[T.slot("surname")],
                        T.span[T.slot("age")],
                    ]
                ]
            ]
        ]
    )
    def __init__(self, dct):
        self.data_dct = dct
        rend.Page.__init__(self)

dct = [{'name':'Mark',
        'surname':'White',
        'age':'45'},
       {'name':'Valentino',
        'surname':'Volonghi',
        'age':'21'},
       {'name':'Peter',
        'surname':'Parker',
        'age':'Unknown'}
      ]

site = appserver.NevowSite(
    Pg(dct)
)
 
application = service.Application("example")
internet.TCPServer(8080, site).setServiceParent(application)
