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
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render_new_post(self, subject="",content="",error=""):
        self.render("new_post.html",content=content, subject=subject, error=error)

    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        self.render("blog.html", posts=posts)

    def render_post(self, post_id):
        post = Post.get_by_id(int(post_id))
        self.render("post.html", post=post)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
class MainPage(BaseHandler):
    def get(self):
        self.render_front()

class NewPostHandler(BaseHandler):
    def get(self):
        self.render_new_post()
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = Post(subject = subject, content = content)
            post.put()
            self.redirect("/blog/"+str(post.key().id()))
        else:
            error = "we need both a subject and content!"
            self.render_new_post(subject,content,error)

class PostHandler(BaseHandler):
    def get(self, post_id):
        self.render_post(post_id)

app = webapp2.WSGIApplication([ 
    ('/', MainPage),
    ('/newpost', NewPostHandler),
    ('/blog/(\d+)', PostHandler)
], debug=True)
