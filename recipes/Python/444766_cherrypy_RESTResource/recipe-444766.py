"""
REST Resource

cherrypy controller mixin to make it easy to build REST applications.

handles nested resources and method-based dispatching.

here's a rough sample of what a controller would look like using this:

cherrypy.root = MainController()
cherrypy.root.user = UserController()

class PostController(RESTResource):
    def index(self,post):
        return post.as_html()
    index.expose_resource = True

    def delete(self,post):
        post.destroySelf()
        return "ok"
    delete.expose_resource = True

    def update(self,post,title="",body=""):
        post.title = title
        post.body = body
        return "ok"
    update.expose_resource = True

    def add(self, post, title="", body="")
        post.title = title
        post.body = body
        return "ok"
    update.expose_resource = True

    def REST_instantiate(self, slug):
        try:
            return Post.select(Post.q.slug == slug, Post.q.userID = self.parent.id)[0]
        except:
            return None

    def REST_create(self, slug):
        return Post(slug=slug,user=self.parent)

class UserController(RESTResource):
    REST_children = {'posts' : PostController()}

    def index(self,user):
        return user.as_html()
    index.expose_resource = True

    def delete(self,user):
        user.destroySelf()
        return "ok"
    delete.expose_resource = True

    def update(self,user,fullname="",email=""):
        user.fullname = fullname
        user.email = email
        return "ok"
    update.expose_resource = True

    def add(self, user, fullname="", email=""):
        user.fullname = fullname
        user.email = email
        return "ok"
    add.expose_resource = True

    def extra_action(self,user):
        # do something else
    extra_action.expose_resource = True

    def REST_instantiate(self, username):
        try:
            return User.byUsername(username)
        except:
            return None

    def REST_create(self, username):
        return User(username=username)

then, the site would have urls like:

    /user/bob
    /user/bob/posts/my-first-post
    /user/bob/posts/my-second-post

which represent REST resources. calling 'GET /usr/bob' would call the index() method on UserController
for the user bob. 'PUT /usr/joe' would create a new user with username 'joe'. 'DELETE /usr/joe'
would delete that user. 'GET /usr/bob/posts/my-first-post' would call index() on the Post Controller
with the post with the slug 'my-first-post' that is owned by bob.


"""


import cherrypy
class RESTResource:
    # default method mapping. ie, if a GET request is made for
    # the resource's url, it will try to call an index() method (if it exists);
    # if a PUT request is made, it will try to call an add() method.
    # if you prefer other method names, just override these values in your
    # controller with REST_map
    REST_defaults = {'DELETE' : 'delete',
                     'GET' : 'index',
                     'POST' : 'update',
                     'PUT' : 'add'}
    REST_map = {}
    # if the resource has children resources, list them here. format is
    # a dictionary of name -> resource mappings. ie,
    #
    # REST_children = {'posts' : PostController()}

    REST_children = {}

    def REST_dispatch(self, resource, **params):
        # if this gets called, we assume that default has already
        # traversed down the tree to the right location and this is
        # being called for a raw resource
        method = cherrypy.request.method
        if self.REST_map.has_key(method):
            m = getattr(self,self.REST_map[method])
            if m and getattr(m, "expose_resource"):
                return m(resource,**params)
        else:
            if self.REST_defaults.has_key(method):
                m = getattr(self,self.REST_defaults[method])
                if m and getattr(m, "expose_resource"):
                    return m(resource,**params)

        raise cherrypy.NotFound

    @cherrypy.expose
    def default(self, *vpath, **params):
        if not vpath:
            return self.list(**params)
        # Make a copy of vpath in a list
        vpath = list(vpath)
        atom = vpath.pop(0)

        # Coerce the ID to the correct db type
        resource = self.REST_instantiate(atom)
        if resource is None:
            if cherrypy.request.method == "PUT":
                # PUT is special since it can be used to create
                # a resource
                resource = self.REST_create(atom)
            else:
                raise cherrypy.NotFound

        # There may be further virtual path components.
        # Try to map them to methods in children or this class.
        if vpath:
            a = vpath.pop(0)
            if self.REST_children.has_key(a):
                c = self.REST_children[a]
                c.parent = resource
                return c.default(*vpath, **params)
            method = getattr(self, a, None)
            if method and getattr(method, "expose_resource"):
                return method(resource, *vpath, **params)
            else:
                # path component was specified but doesn't
                # map to anything exposed and callable
                raise cherrypy.NotFound

        # No further known vpath components. Call a default handler
        # based on the method
        return self.REST_dispatch(resource,**params)

    def REST_instantiate(self,id):
        """ instantiate a REST resource based on the id

        this method MUST be overridden in your class. it will be passed
        the id (from the url fragment) and should return a model object
        corresponding to the resource.

        if the object doesn't exist, it should return None rather than throwing
        an error. if this method returns None and it is a PUT request,
        REST_create() will be called so you can actually create the resource.
        """
        raise cherrypy.NotFound

    def REST_create(self,id):
        """ create a REST resource with the specified id

        this method should be overridden in your class.
        this method will be called when a PUT request is made for a resource
        that doesn't already exist. you should create the resource in this method
        and return it.
        """
        raise cherrypy.NotFound
