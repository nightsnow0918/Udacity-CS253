import string
import hashlib
import random

def hash_str_scramble(name, pw, salt):
    return pw+salt+name

def make_salt():
    return "".join([random.choice(string.letters) for x in xrange(5)])

def gen_hash_pw(pw, secret):
    if pw and secret:
        return hashlib.sha256(secret+pw).hexdigest()

def gen_hash_cookie(name, pw, salt):
    h = ""
    if not salt:
        salt = make_salt()
    hash_str = hash_str_scramble(name, pw, salt)
    h = "%s|%s" % (hashlib.sha256(hash_str).hexdigest(), salt)
    return h

def valid_cookie(name, pw, h):
    salt = h.split("|")[1]
    return gen_hash_cookie(name, pw, salt) == h
