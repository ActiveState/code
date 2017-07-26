#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Dan McDougall
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Meta
__version__ = '1.0'
__license__ = "Apache License, Version 2.0"
__version_info__ = (1, 0)
__author__ = 'Dan McDougall <YouKnowWho@YouKnowWhat.com>'

"""
Tornado MethodDispatcher
========================
The MethodDispatcher is a subclass of tornado.web.RequestHandler that will use
the methods contained in subclasses of MethodDispatcher to handle requests.  In
other words, instead of having to make a new RequestHandler class for every URL
in your application you can subclass MethodDispatcher and use the methods
contained therein *as* your URLs.

The MethodDispatcher also adds the convenience of automatically passing
arguments to your class methods.  So there is no need to use Tornado's
get_argument() method.

Example
-------
To demonstrate the advantages of using MethodDispatcher I'll present a standard
Tornado app with multiple URLs and re-write it using MethodDispatcher...

The standard Tornado way
------------------------
    class Foo(tornado.web.RequestHandler):
        def get(self):
            self.write('foo')

    class Bar(tornado.web.RequestHandler):
        def get(self):
            self.write('bar')

    class SimonSays(tornado.web.RequestHandler):
        def get(self):
            say = self.get_argument("say")
            self.write('Simon says, %s' % `say`)

    application = tornado.web.Application([
        (r"/foo", Foo),
        (r"/bar", Bar),
        (r"/simonsays", SimonSays),
    ])

The MethodDispatcher way
------------------------
    class FooBar(MethodDispatcher):
        def foo(self):
            self.write("foo")

        def bar(self):
            self.write("bar")

        def simonsays(self, say):
            self.write("Simon Says, %s" % `say`)

    application = tornado.web.Application([
        (r"/.*", FooBar)
    ])

Notes
-----
As you can see from the above example, using the MethodDispatcher can
significantly reduce the complexity of Tornado applications.  Here's some other
things to keep in mind when using the MethodDispatcher:

 * MethodDispatcher will ignore any methods that begin with an underscore (_).
   This prevents builtins and private methods from being exposed to the web.
 * The '/' path is special: It always maps to self.index().
 * MethodDispatcher does not require that your methods distinquish between GET
   and POST requests.  Whether a GET or POST is performed the matching method
   will be called with any passed arguments or POSTed data.  Because of the way
   this works you should not use get() and post() in your MethodDispatcher
   subclasses unless you want to override this functionality.
 * When an argument is passed with a single value (/simonsays?say=hello) the
   value passed to the argument will be de-listed.  In other words, it will be
   passed to your method like so:  {'say': 'hello'}.  This overrides the
   default Tornado behavior which would return the value as a list:
   {'say': ['hello']}.  If more than one value is passed MethodDispatcher will
   use the default behavior.
"""

import tornado.web

def delist_arguments(args):
    """
    Takes a dictionary, 'args' and de-lists any single-item lists then
    returns the resulting dictionary.

    In other words, {'foo': ['bar']} would become {'foo': 'bar'}
    """
    for arg, value in args.items():
        if len(value) == 1:
            args[arg] = value[0]
    return args

class MethodDispatcher(tornado.web.RequestHandler):
    """
    Subclasss this to have all of your class's methods exposed to the web
    for both GET and POST requests.  Class methods that start with an
    underscore (_) will be ignored.
    """

    def _dispatch(self):
        """
        Load up the requested URL if it matches one of our own methods.
        Skip methods that start with an underscore (_).
        """
        args = None
        # Sanitize argument lists:
        if self.request.arguments:
            args = delist_arguments(self.request.arguments)
        # Special index method handler:
        if self.request.uri.endswith('/'):
            func = getattr(self, 'index', None)
            if args:
                return func(**args)
            else:
                return func()
        path = self.request.uri.split('?')[0]
        method = path.split('/')[-1]
        if not method.startswith('_'):
            func = getattr(self, method, None)
            if func:
                if args:
                    return func(**args)
                else:
                    return func()
            else:
                raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)

    def get(self):
        """Returns self._dispatch()"""
        return self._dispatch()

    def post(self):
        """Returns self._dispatch()"""
        return self._dispatch()

class TestMethodDispatcher(MethodDispatcher):
    """
    This class demonstrates how to use MethodDispatcher() to load URLs based
    on the names of the methods in a class.  It also demonstrates the special
    index handler and how arguments are passed to methods.
    """
    def index(self):
        self.write(
            "The special index handler has been called.<br />"
            "Try <a href='testing?foo=bar&say=hello'>"
            "testing?foo=bar&say=hello</a>"
        )

    def testing(self, **kwargs):
        self.write("testing() got the following arguments: %s" % `kwargs`)

class TestApplication(tornado.web.Application):
    """
    This Tornado Application container demonstrates how to include a
    MethodDispatcher class in your app via a catch-all regular expression.
    """
    def __init__(self):
        handlers = [
            # Basic catch-all URL handler:
            (r"/.*", TestMethodDispatcher),
            # You can also use a MethodDispatcher in sub-paths:
            (r"/test/.*", TestMethodDispatcher)
        ]
        tornado.web.Application.__init__(self, handlers)

def test_method_dispatcher():
    """
    This function can be used to test that the MethodDispatcher is working
    properly. It is called automatically when this script is executed directly.
    """
    import logging
    from tornado.ioloop import IOLoop
    from tornado.httpserver import HTTPServer
    from tornado.options import define, options, parse_command_line
    define("port", default=8888, help="Run on the given port", type=int)
    parse_command_line()
    logging.info(
        "Test Server Listening on http://0.0.0.0:%s/" % options.port
    )
    http_server = HTTPServer(TestApplication())
    http_server.listen(options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    test_method_dispatcher()
