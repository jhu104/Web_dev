from BaseHandler import BaseHandler
from datetime import datetime

class MainHandler(BaseHandler):
    def render_front(self):
        (posts, last_updated) = self.top_posts()
        current_time = datetime.now()
        difference = current_time - last_updated

        if self.format == 'html':
            self.render("blog.html", posts=posts, seconds=difference.total_seconds())
        else:
            return self.render_json([post.as_dict() for post in posts])

    def get(self):
        self.render_front()