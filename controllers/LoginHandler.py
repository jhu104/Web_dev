from BaseHandler import BaseHandler
from security import hashing
from models.User import User

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            self.login(user)
            self.redirect("/welcome")
        else:
            self.render("login.html", error="Invalid login")
