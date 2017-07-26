# Importing the necessary classes from Google App Engine.
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        
        if user:
            welcome = ("Welcome, %s! (<a href='%s'>Sing out</a>)"
                        % (user.nickname(), users.create_logout_url('/')))
        else:
            welcome = ("<a href='%s'>Sign in or Register</a>"
                        % users.create_login_url('/'))
        
        self.response.out.write("<html><head><title>Web App Title</title></head><body>%s</body></html>"
                                % welcome)

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug = True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
