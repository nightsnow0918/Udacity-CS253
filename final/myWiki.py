#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import re
import json
import time
import logging

import jinja2, webapp2

from lib import webhash

from google.appengine.api import memcache
from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


################### WiKi Pages ####################
class WikiPost(db.Model):

    pagename = db.TextProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now=True)


class MainPage(Handler):

    def get(self):
        self.render('myWiki.html', status='logout')


class WikiPageHandler(Handler):
    
    def get(self, pagename):
        pass


class EditWikiPageHandler(Handler):

    def get(self, pagename):
        pass


################### Sign-Up Handling ####################
USER_RE     = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWD_RE   = re.compile("^.{3,20}$")
EMAIL_RE    = re.compile("^[\S]+@[\S]+\.[\S]+$")

SECRET = "6xhgj$ad3.@qozalb&jd!7iso0126udvn3m#f"

class UserProfile(db.Model):
    name    = db.StringProperty(required=True)
    password= db.StringProperty()


def valid_username(name):
    return USER_RE.match(name)

def valid_password(password):
    return PASSWD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)


class SignUpPage(Handler):

    def valid_input(self, username, password, verify, email):
        valid = True

        if not username or not valid_username(username):
            self.param["err_username"] = "Invalid user name"
            valid = False
        elif self.chk_user_exist(username):
            self.param["err_username"] = "Username already exists"
            valid = False
        else:
            self.param["username"] = username

        if not password or not valid_password(password):
            self.param["err_password"] = "Invalid password"
            valid = False

        if password != verify:
            self.param["err_vry_password"] = "The password didn't match"
            self.param["password"]         = ""
            self.param["verify"]           = ""
            valid = False

        if email and not valid_email(email):
            self.param["err_email"] = "The email address" 
            valid = False
        else:
            self.param["email"] = email

        return valid
    
    def chk_user_exist(self, user):
        return UserProfile.gql("WHERE name=:1", user).get()

    def get(self):
        self.render('signup.html', signup_dest='/mywiki/signup')

    def post(self):
        username   = self.request.get('username')
        password   = self.request.get('password')
        verify     = self.request.get('verify')
        email      = self.request.get('email')

        self.param = dict(username=username, email=email, 
                          signup_dest='/mywiki/signup')

        if self.valid_input(username, password, verify, email):
            # Generate hash strings
            hash_pw     = webhash.gen_hash_pw(password, SECRET)
            hash_cookie = webhash.gen_hash_cookie(username, hash_pw, salt='')

            # Store username/password into database
            new_user = UserProfile(name=username, password=hash_pw)
            new_user.put()

            # Set Cookie
            self.response.set_cookie('name', value=hash_cookie, path='/')
            
            # Redirect to welcome page
            time.sleep(1)
            self.redirect('/mywiki')
        else:
            self.render('signup.html', **self.param)


class LoginPage(Handler):

    def get(self):
        self.render('login.html', login_dest='/mywiki/login')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        self.param = dict(username=username, password=password)

        user_list = UserProfile.all()
        for user in user_list:
            if username==user.name:
                if webhash.gen_hash_pw(password, SECRET)!=user.password:
                    self.param['err_password'] = "Invalid Password"
                    self.render('login.html', **self.param)
                else:
                    self.redirect('/mywiki')
                break
        else:
            self.param['err_username'] = "User does not exist"
            self.render('login.html', **self.param)


class Logout(Handler):

    def get(self):
        self.response.set_cookie('name', value='', path='/')
        self.redirect('/mywiki/signup')
            
