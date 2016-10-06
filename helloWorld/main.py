import webapp2
import os
import jinja2
import cgi 
import re 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

form="""
<form method="post">
    What is your birthday?
    <br>
    <lable>Month<input type="text" name="month" value=%(month)s></label>
    <lable>Day<input type="text" name="day" value=%(day)s></label>
    <lable>Year<input type="text" name="year" value=%(year)s></label>
    <div style="color:red">%(error)s</div>
    <br>
    <input type="submit">
</form>
"""

rot13_form="""
<form method="post">
<h1>Enter some text to ROT13:</h1>
<textarea name="text">%(data)s</textarea>
<input type="submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_month(month):
    if month.isdigit():
        month = int(month)
        if month <= 12 and month >= 1:
            return month

def valid_day(day):
    if day.isdigit():
        day = int(day)
        if day <= 31 and day >= 1:
            return day
def valid_year(year):
    if year.isdigit():
        year = int(year)
        if(year >= 1900 and year < 2020):
            return year
class BaseHandler(webapp2.RequestHandler):
    def render_front(self, template, email="",username="",error=""):
        self.render(template,email=email,error=error,username=username)
    
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", year="", day="", month=""):
        self.response.out.write(form % {"error": error, "month":escape_html(month),"year": escape_html(year),"day": escape_html(day)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_year = self.request.get('year')
        user_day = self.request.get('day')

        month = valid_month(user_month)
        year = valid_year(user_year)
        day = valid_day(user_day)

        if not ((user_month and user_day and user_year) and (month and day and year)):
            self.write_form("That doesn't look valid to me, friend.", month=user_month, year=user_year, day=user_day)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")
        
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

class Rot13Handler(webapp2.RequestHandler):
    def write_form(self, data=""):
        self.response.out.write(rot13_form % {"data":escape_html(data)})

    def rot13(self, data):
        rot13 = ""
        for char in data:
            char_num = ord(char)
            if char_num >= ord('A') and char_num <= ord('z'):
                if char_num >= ord('A') and char_num <= ord('Z'):
                    new_char_num = (char_num-ord('A')+13)%26
                    rot13 += chr(new_char_num+ord('A'))
                else:
                    new_char_num = (char_num-ord('a')+13)%26
                    rot13 += chr(new_char_num+ord('a'))
            else:
                rot13 += char

        return rot13

    def get(self):
        self.write_form()

    def post(self):
        data = self.request.get('text')
        res = self.rot13(data)
        self.write_form(res)

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
        self.render_front("signup.html")

    def post(self):
        username =  self.request.get("username")
        password =  self.request.get("password")
        verify =    self.request.get("verify")
        email =     self.request.get("email")

        valid = True
        error = {}

        v_username =    self.valid_username(username)
        v_password =    self.valid_password(password)
        v_email =       self.valid_email(email)
        print(v_username)
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
            print(username)
            self.render_front("signup.html", email=email, username=username, error=error)
        else:
            self.redirect("/welcome?username="+username)

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("username")
        self.response.write("<h2>Welcome "+username+"!</h2>")

app = webapp2.WSGIApplication([ ('/', MainPage), 
                                ('/thanks', ThanksHandler), 
                                ('/rot13', Rot13Handler),
                                ('/signup', SignupHandler),
                                ('/welcome', SuccessHandler)],debug=True)
