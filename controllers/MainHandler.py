from BaseHandler import BaseHandler
from google.appengine.ext import db

class MainHandler(BaseHandler):
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        posts = list(posts)

        if self.format == 'html':
            self.render("blog.html", posts=posts)
        else:
            return self.render_json([post.as_dict() for post in posts])

    def get(self):
        self.render_front()