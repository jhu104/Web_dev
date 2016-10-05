import webapp2
import os
import jinja2
import cgi 
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

app = webapp2.WSGIApplication([ ('/', MainPage), ('/thanks', ThanksHandler), ('/rot13', Rot13Handler)],debug=True)
