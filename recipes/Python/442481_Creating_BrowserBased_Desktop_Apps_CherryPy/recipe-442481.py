import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
        return "Hello, world! <br /><a href='stop'>Stop</a>"
    # index.exposed = True # for python < 2.4

    @cherrypy.expose
    def stop(self):
        raise SystemExit
    # stop.exposed = True

if __name__ == '__main__':

    import webbrowser

    cherrypy.root = Root()

    cherrypy.config.update({
            'server.environment':'production',
            'server.socketHost':'127.0.0.1',
            })

    cherrypy.server.start_with_callback(
            webbrowser.open,
            ('http://localhost:8080',),
            )
