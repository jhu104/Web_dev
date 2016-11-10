from BaseHandler import BaseHandler
from models.Post import Post

class NewPostHandler(BaseHandler):
    def render_new_post(self, subject="",content="",error=""):
        self.render("new_post.html",content=content, subject=subject, error=error)

    def get(self):
        self.render_new_post()
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = Post(subject = subject, content = content)
            post.put()
            self.redirect("/blog/"+str(post.key().id()))
        else:
            error = "we need both a subject and content!"
            self.render_new_post(subject,content,error)