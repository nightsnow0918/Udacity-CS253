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

import jinja2
import webapp2
from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

class Article(db.Model):
    index   = db.IntegerProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class NewPostHandler(Handler):

    total_articles = 0

    def valid_input(self, subject, content):
        return subject and content

    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if not self.valid_input(subject, content):
            self.render("newpost.html", subject=subject,
                                        content=content,
                                        err_input="Required subject and contents!")
        else:
            total_articles = db.GqlQuery("Select * from Article").count()
            new_article = Article(subject=subject, content=content, 
                                  index=total_articles+1)
            new_article.put()
            
            self.redirect("/unit3/myblog/"+str(total_articles+1))


class PostHandler(Handler):
    
    def get(self, post_id):
        article = None
        # data may not have been stored into database, keep querying until get the result
        while not article: 
            article = db.GqlQuery("Select * from Article where index="+post_id).get()
        self.render("article.html", subject=article.subject, content=article.content)


class MyBlogMainHandler(Handler):

    def get(self):
        articles = db.GqlQuery("Select * from Article ORDER BY index DESC")
        self.render("myBlog.html", articles=articles)


################### Sign-Up Handling ####################
USER_RE     = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWD_RE   = re.compile("^.{3,20}$")
EMAIL_RE    = re.compile("^[\S]+@[\S]+\.[\S]+$")

def valid_username(name):
    return USER_RE.match(name)

def valid_password(password):
    return PASSWD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

class SignUpHandler(Handler):

    def valid_input(self, username, password, vry_password, email):
        err = False

        if not username or not valid_username(username):
            self.param["err_username"] = "Invalid user name"
            err = True
        else:
            self.param["username"] = username

        if not password or not valid_password(password):
            self.param["err_password"] = "Invalid password"
            err = True

        if password != vry_password:
            self.param["err_vry_password"] = "The password didn't match"
            self.param["password"]         = ""
            self.param["vry_password"]     = ""
            err = True

        if email and not valid_email(email):
            self.param["err_email"] = "The email address" 
            err = True
        else:
            self.param["email"] = email

        return not err
    
    
    def get(self):
        self.render('signup.html')


    def post(self):
        username     = self.request.get('username')
        password     = self.request.get('password')
        vry_password = self.request.get('vry_password')
        email        = self.request.get('email')

        self.param   = dict(username=username, email=email)

        if self.valid_input(username, password, vry_password, email):
            self.response.set_cookie('username', username, path='/')
            self.redirect('/unit3/myblog/welcome')
            pass 
        else:
            self.render('signup.html', **self.param)


class WelcomeHandler(Handler):

    def get(self):
        username = self.request.cookies.get('username')
        self.render('welcome.html', username=username)
        pass

    def post(self):
        pass


