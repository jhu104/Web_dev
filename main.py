'''
Created on May 15, 2016

@author: jay
'''
import webapp2
from controllers.MainHandler import MainHandler
from controllers.LoginHandler import LoginHandler
from controllers.LogoutHandler import LogoutHandler
from controllers.NewPostHandler import NewPostHandler
from controllers.PostHandler import PostHandler
from controllers.SignupHandler import SignupHandler
from controllers.SuccessHandler import SuccessHandler

app = webapp2.WSGIApplication([ 
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/newpost', NewPostHandler),
    ('/blog/([0-9]+)', PostHandler),
    ('/signup', SignupHandler),
    ('/welcome', SuccessHandler)
], debug=True)
