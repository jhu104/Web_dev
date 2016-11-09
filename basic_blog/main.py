'''
Created on May 15, 2012

@author: jay
'''
import webapp2
import os
import jinja2
import re
from security import hashing
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
        if not post:
            self.error(404)
            return
        self.render("post.html", post=post)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
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

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class SignupHandler(BaseHandler):
    def valid_username(self, username):
        return USER_RE.match(username)

    def valid_password(self, password):
        return PASSWORD_RE.match(password)

    def valid_email(self, email):
        return EMAIL_RE.match(email)

    def get(self):
        self.render("signup.html",error="")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        valid = True
        error = {}

        v_username = self.valid_username(username)
        v_password = self.valid_password(password)
        v_email = self.valid_email(email)
        if not v_username or v_username.string != username:
            valid = False
            error["user_error"] = "That's not a valid username."
        if not v_password or v_password.string != password:
            valid = False
            error["valid_pass_error"] = "That's not a valid password."
        if verify != password:
            valid = False
            error["pass_match_error"] = "Your passwords didn't match."
        if len(email) > 0 and (not v_email or v_email.string != email):
            valid = False
            error["email_error"] = "That's not a valid email."

        if not valid:
            self.render("signup.html", email=email, username=username, error=error)
        else:
            user_hash = hashing.make_secure_val(username)
            self.response.headers.add_header('Set-Cookie', str('name='+user_hash+'; Path=/'))
            self.redirect("/welcome")

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        userhash=self.request.cookies.get('name')
        username=userhash.split('|')[0]
        if userhash and hashing.check_secure_val(userhash):
            self.response.write("<h2>Welcome "+username+"!</h2>")
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([ 
    ('/', MainPage),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostHandler),
    ('/signup', SignupHandler),
    ('/welcome', SuccessHandler)
], debug=True)
