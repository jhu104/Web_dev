from controllers.BaseHandler import BaseHandler
from security import hashing

class SuccessHandler(BaseHandler):
    def get(self):
        if self.user:
            self.response.write("<h2>Welcome "+self.user.username+"!</h2>")
        else:
            self.redirect('/signup')