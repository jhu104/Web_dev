'''
Created on May 15, 2012

@author: jay
'''
import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class BaseHandler(webapp2.RequestHandler):
    def render_front(self, title="",art="",error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("asciichan.html",title=title,art=art,error=error,arts=arts)
    
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
class MainPage(BaseHandler):
    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            a.put()
            self.redirect("/")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title,art,error)

app = webapp2.WSGIApplication([ ('/', MainPage)],debug=True)
