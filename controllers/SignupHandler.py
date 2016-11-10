"""
Signup handler
"""
from controllers.BaseHandler import BaseHandler
from security import hashing
from utils import validations
from models.User import User

class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup.html", error="")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        valid = True
        error = {}

        v_username = validations.valid_username(username)
        v_password = validations.valid_password(password)
        v_email = validations.valid_email(email)
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
            user = User.by_name(username)
            if user:
                self.render("signup.html", error={'user_error': "User already exists."})
            else:
                user = User.register(username, password)
                user.put()
                self.login(username)
                self.redirect("/welcome")
                