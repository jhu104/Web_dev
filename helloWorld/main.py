import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello, Udacity!")

app = webapp2.WSGIApplication([ ('/', MainPage)],debug=True)
