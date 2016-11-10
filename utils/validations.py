"""
Util module for validations
"""
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def valid_username(username):
    """function(username) -> bool"""
    return USER_RE.match(username)

def valid_password(password):
    """function(password) -> bool"""
    return PASSWORD_RE.match(password)

def valid_email(email):
    """function(email) -> bool"""
    return EMAIL_RE.match(email)

