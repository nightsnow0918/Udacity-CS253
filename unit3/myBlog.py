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

import jinja2
import webapp2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
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

class NewPostHandler(Handler):

    def valid_input(self, subject, content):
        return subject and content

    def get(self):
        self.render("myBlog.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        app = webapp2.WSGIApplication(debug=True)
        app.router.add(('/unit3/myBlog/tmp','tmpHandler'))
        if not self.valid_input(subject, content):
            self.render("myBlog.html", subject=subject,
                                       content=content,
                                       err_input="Required subject and contents!")
        else:
            self.redirect("/unit3/myBlog/tmp?subject="+subject)

class tmpHandler(Handler):
    def get(self):
        subject = self.request.get("subject")
        self.write(subject)

class MyBlogMainHandler(Handler):
    def get(self):
        pass

    def post(self):
        pass


