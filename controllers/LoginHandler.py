from BaseHandler import BaseHandler
from security import hashing
from google.appengine.ext import db

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = db.GqlQuery("SELECT * FROM User WHERE username='"+username+"'")[0]
        if user:
            user_password=user.password
            if hashing.valid_pw(username, password, user_password):
                user_hash = hashing.make_secure_val(username)
                self.response.headers.add_header('Set-Cookie', str('name='+user_hash+'; Path=/'))
                self.redirect("/welcome")
            else:
                self.render("login.html", error="Invalid login")
        else:
            self.render("login.html", error="Invalid login")
