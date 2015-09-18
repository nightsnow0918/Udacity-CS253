import string
import hashlib
import random

def hash_str_scramble(name, pw, salt):
    return pw+salt+name

def gen_hash_string(name, pw, salt):
    h = ""
    if not salt:
        salt = "".join([random.choice(string.letters) for x in xrange(5)])
    hash_str = hash_str_scramble(name, pw, salt)
    h = "%s|%s" % (hashlib.sha256(hash_str).hexdigest, salt)
    return h

def check_hash_valid(name, pw, h):
    salt = h.split("|")[1]
    return gen_hash_string(name, pw, salt) == h
