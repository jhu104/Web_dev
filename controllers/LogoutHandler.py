from BaseHandler import BaseHandler
from security import hashing
from google.appengine.ext import db

class LogoutHandler(BaseHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect('/signup')