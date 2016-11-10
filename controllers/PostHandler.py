from BaseHandler import BaseHandler
from models.Post import Post

class PostHandler(BaseHandler):
    def render_post(self, post_id):
        post = Post.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        self.render("post.html", post=post)

    def get(self, post_id):
        self.render_post(post_id)