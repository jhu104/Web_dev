import webapp2
import jinja2
import os
from security import hashing
from models.User import User
from models.Post import Post
import json
from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import datetime

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, jsonData):
        json_txt = json.dumps(jsonData)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = hashing.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val)
        )
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and hashing.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('json'):
            self.format = 'json'
        else:
            self.format = 'html'
        self.client = memcache.Client()
        
    def top_posts(self, update=False):
        key = 'top'
        last_update_key = 'lastupdate'
        posts = self.client.get(key)
        last_update = self.client.get(last_update_key)
        if posts is None or update:
            posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
            posts = list(posts)
            result = self.client.set(key, posts)
            if result:
                last_update = datetime.now()
                last_update = last_update.strftime('%b %d %Y %I:%M%p')
                self.client.set(last_update_key, last_update)
        last_update = datetime.strptime(last_update, '%b %d %Y %I:%M%p')
        
        return (posts, last_update)
    
    def post(self, id, update=False):
        post_id = int(id)
        post = self.client.get(id)
        last_update = self.client.get(str(id)+'u')
        if post is None or update:
            post = Post.get_by_id(post_id)
            self.client.set(id, post)
            last_update = datetime.now()
            last_update = last_update.strftime('%b %d %Y %I:%M%p')
            self.client.set(str(id)+'u', last_update)
        last_update = datetime.strptime(last_update, '%b %d %Y %I:%M%p')
        return (post, last_update)

    def clearCache(self):
        self.client.flush_all()
        self.redirect('/')
