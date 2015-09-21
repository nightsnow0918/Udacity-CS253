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
import webapp2
from unit2 import hw1
from unit2 import hw2
from unit3 import myBlog

class MainHandler(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/', MainHandler), 
    ('/unit2/hw1', hw1.Hw1MainHandler),
    ('/unit2/hw2', hw2.Hw2MainHandler), 
    ('/unit2/hw2/welcome', hw2.HelloHandler),
    ('/unit3/myblog', myBlog.MyBlogMainPage),
    ('/unit3/myblog/signup', myBlog.SignUpPage),
    ('/unit3/myblog/welcome', myBlog.WelcomePage),
    ('/unit3/myblog/newpost', myBlog.NewPostPage),
    ('/unit3/myblog/(\d+)', myBlog.Permalinks)
], debug=True)
