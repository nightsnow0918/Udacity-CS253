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
from unit2 import hw2

HW1_HTML = """
<form method="post" action="/unit2/hw1">
<h3>Enter your string for ROT13</h3>
<textarea name="text" rows="5px" cols="50px">%(rot13_text)s</textarea><BR>
<input type="submit" name="Submit">
</form>
"""

def escape_html(s):
    for (i,o) in (('&','&amp;'), ('>','&gt;'), ('<','&lt;'), ('"','&quot;')):
        s = s.replace(i,o)
    return s
                
def rot13_trans(s):
    rot_s = ""
    for c in s:
        ord_c = ord(c)
        if 65<=ord_c<=90: 
            rot_s += chr( (ord_c-65+13)%26 + 65 )
        elif 97<=ord_c<=122:
            rot_s += chr( (ord_c-97+13)%26 + 97 )
        else:
            rot_s += c
    return rot_s

class Hw1MainHandler(webapp2.RequestHandler):
    def write_form(self, rot13_text=""):
        self.response.out.write(HW1_HTML % {"rot13_text":rot13_text})

    def get(self):
        self.write_form()

    def post(self):
        rot13 = rot13_trans(self.request.get("text"))
        self.write_form(rot13_text=escape_html(rot13))

