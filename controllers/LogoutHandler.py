from BaseHandler import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')
