from BaseHandler import BaseHandler
from google.appengine.ext import db

class MainHandler(BaseHandler):
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        self.render("blog.html", posts=posts)

    def get(self):
        self.render_front()