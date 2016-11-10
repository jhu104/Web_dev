import webapp2
from security import hashing

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        userhash=self.request.cookies.get('name')
        username=userhash.split('|')[0]
        if userhash and hashing.check_secure_val(userhash):
            self.response.write("<h2>Welcome "+username+"!</h2>")
        else:
            self.redirect('/signup')