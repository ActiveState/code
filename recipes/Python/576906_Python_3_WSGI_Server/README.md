## Python 3 WSGI Server  
Originally published: 2009-09-19 06:11:33  
Last updated: 2009-09-22 11:36:30  
Author: poops mcgee  
  
This is a simplified version of tornado's WSGI server implemented in python 3.

Example usage:

    import web
    import wsgiref.simple_server

    class MainHandler(web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    if __name__ == "__main__":
        application = web.WSGIApplication([
            (r"/", MainHandler),
        ])
        server = wsgiref.simple_server.make_server('', 8888, application)
        server.serve_forever()