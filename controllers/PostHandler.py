from BaseHandler import BaseHandler
from datetime import datetime

class PostHandler(BaseHandler):
    def render_post(self, post_id, update=False):
        (post, last_updated) = self.post(post_id)
        current_time = datetime.now()
        difference = current_time - last_updated

        if not post:
            self.error(404)
            return
        if self.format == 'html':
            self.render("post.html", post=post, seconds=difference.total_seconds())
        else:
            return self.render_json(post.as_dict())

    def get(self, post_id):
        self.render_post(post_id)
