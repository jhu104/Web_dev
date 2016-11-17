from BaseHandler import BaseHandler

class FlushHandler(BaseHandler):
    def get(self):
        self.clearCache()
