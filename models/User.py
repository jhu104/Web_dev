from google.appengine.ext import db
from security import hashing

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = hashing.users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def login(cls, name, password):
        u = cls.by_name(name)
        if u and hashing.valid_pw(name, password, u.password):
            return u

    @classmethod
    def register(cls, username, pw, email = None):
        pw_hash = hashing.make_pw_hash(username, pw)
        return User(parent = hashing.users_key(),
                    username = username,
                    password = pw_hash,
                    email = email)
