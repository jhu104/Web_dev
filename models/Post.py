from google.appengine.ext import db

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def as_dict(self):
        time_fmt = '%c'
        data = {'subject': self.subject,
                'content': self.content,
                'created': self.created.strftime(time_fmt),
                'last_modified': self.last_modified.strftime(time_fmt)
               }
        return data
