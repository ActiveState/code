## Method-based URL dispatcher for the Tornado web server  
Originally published: 2009-11-17 08:42:29  
Last updated: 2009-11-20 11:51:47  
Author: Dan McDougall  
  
The MethodDispatcher is a subclass of [tornado](http://www.tornadoweb.org/).web.RequestHandler that will use
the methods contained in subclasses of MethodDispatcher to handle requests.  In
other words, instead of having to make a new RequestHandler class for every URL
in your application you can subclass MethodDispatcher and use the methods
contained therein *as* your URLs.

The MethodDispatcher also adds the convenience of automatically passing
arguments to your class methods.  So there is no need to use Tornado's
get_argument() method.

**Example**
-------
To demonstrate the advantages of using MethodDispatcher I'll present a standard
Tornado app with multiple URLs and re-write it using MethodDispatcher...

**The standard Tornado way**
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

**The MethodDispatcher way**
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

**Notes**
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