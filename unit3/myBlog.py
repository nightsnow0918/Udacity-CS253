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
        pass


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

class ErrorFormMsg():
    
    def __init__(self, err_user, err_passwd, err_vrfy_passwd, err_email):
        self.err_user        = err_user
        self.err_passwd      = err_passwd
        self.err_vrfy_passwd = err_vrfy_passwd
        self.err_email       = err_email

class SignUpHandler(Handler):

    def valid_input(self):
        err = False
        if not self.username or not valid_username(self.username):
            self.err_msg.err_user = "Invalid user name"
            err = True
        else:
            self.username = username

        if not self.password or not valid_password(self.password):
            self.err_passwd = "Invalid pass word"
            err = True

        if self.passwd != self.vrfy_passwd:
            self.err_vrfy_passwd = "The password didn't match"
            self.passwd = ""
            self.vrfy_passwd = ""
            err = True

        if self.email and not valid_email(self.email):
            self.err_email = "The email address" 
            err = True

        return err
    
    
    def get(self):
        self.render('signup.html')


    def post(self):
        self.username     = self.request.get('username')
        self.password     = self.request.get('password')
        self.vry_password = self.request.get('vry_password')
        self.email        = self.request.get('email')

        self.err_msg = ErrorFormMsg(err_user="", err_passwd="",
                                    err_vrfy_passwd="", err_email="")
        if self.valid_input(self):
            pass
        else:
            pass



