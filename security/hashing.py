import hmac
import hashlib
import random
import string
from google.appengine.ext import db

SECRET = 'imsosecret'
def hash_str(str):
    """hash_str(str) -> str"""
    return hmac.new(SECRET, str).hexdigest()

def make_secure_val(string):
    """make_secure_val(str) -> str"""
    return "%s|%s" % (string, hash_str(str))

def check_secure_val(hash):
    """check_secure_val(hash) -> int"""
    val = hash.split('|')[0]
    if hash == make_secure_val(val):
        return val

def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))
    
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name+pw+salt).hexdigest()
    return "%s|%s" % (h, salt)

def valid_pw(name, pw, hash):
    salt = hash.split('|')[1]
    return hash == make_pw_hash(name, pw, salt=salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)
