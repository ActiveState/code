## Python 3 WSGI Server  
Originally published: 2009-09-19 06:11:33  
Last updated: 2009-09-22 11:36:30  
Author: poops mcgee  
  
This is a simplified version of tornado's WSGI server implemented in python 3.\n\nExample usage:\n\n    import web\n    import wsgiref.simple_server\n\n    class MainHandler(web.RequestHandler):\n        def get(self):\n            self.write("Hello, world")\n\n    if __name__ == "__main__":\n        application = web.WSGIApplication([\n            (r"/", MainHandler),\n        ])\n        server = wsgiref.simple_server.make_server('', 8888, application)\n        server.serve_forever()