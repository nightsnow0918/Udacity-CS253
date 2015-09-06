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
import re

HW2_HTML = """
<form method="post" action="/unit2/hw2">
    <label>Username
        <input type="text" name="usrname" value="%(user)s">
    </label>
    <div style="color:red">%(err_user)s</div><BR>
    <label>Password
        <input type="text" name="passwd" value="%(passwd)s">
    </label>
    <div style="color:red">%(err_passwd)s</div><BR>
    <label>Verify Password
        <input type="text" name="vrfy_passwd" value="%(vrfy_passwd)s">
    </label>
    <div style="color:red">%(err_vrfy_passwd)s</div><BR>
    <label>Email(optional)
        <input type="text" name="email" value="%(email)s">
    </label>
    <div style="color:red">%(err_email)s</div><BR>
    <input type="submit">
</form>
"""

USER_RE         = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWD_RE       = re.compile("^.{3,20}$")
EMAIL_RE        = re.compile("^[\S]+@[\S]+\.[\S]+$")

class Hw2MainHandler(webapp2.RequestHandler):

    usrname=""

    def write_form(self,err_user="",err_passwd="",err_vrfy_passwd="",err_email="",
                        usrname="",passwd="",vrfy_passwd="",email=""):
        self.response.write(HW2_HTML % {"err_user"          :err_user,
                                    "err_passwd"        :err_passwd,
                                    "err_vrfy_passwd"   :err_vrfy_passwd,
                                    "err_email"         :err_email,
                                    "user"              :usrname,
                                    "passwd"            :passwd,
                                    "vrfy_passwd"       :vrfy_passwd,
                                    "email"             :email})

    def valid_usrname(self, name):
        return USER_RE.match(name)

    def valid_passwd(self, passwd):
        return PASSWD_RE.match(passwd)

    def valid_email(self, email):
        return EMAIL_RE.match(email)

    def get(self):
        self.write_form()

    def post(self):
        usrname     = self.request.get("usrname")
        passwd      = self.request.get("passwd")
        vrfy_passwd = self.request.get("vrfy_passwd")
        email       = self.request.get("email")
        err_user    = ""
        err_passwd  = ""
        err_vrfy_passwd = ""
        err_email   = ""

        if not usrname or not self.valid_usrname(usrname):
            err_user = "Invalid user name"
        else:
            Hw2MainHandler.usrname = usrname

        if not passwd or not self.valid_passwd(passwd):
            err_passwd = "Invalid pass word"

        if passwd != vrfy_passwd:
            err_vrfy_passwd = "The password didn't match"
            passwd = ""
            vrfy_passwd = ""

        if email and not self.valid_email(email):
            err_email = "The email address" 

        if not err_user and not err_passwd and not err_vrfy_passwd and not err_email:
            self.redirect("/unit2/hw2/welcome",body=usrname)
        else:
            self.write_form(err_user=err_user, err_passwd=err_passwd, err_vrfy_passwd=err_vrfy_passwd, err_email=err_email,
                            usrname=usrname, passwd=passwd, vrfy_passwd=vrfy_passwd, email=email)

class HelloHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Welcome, %s!" % Hw2MainHandler.usrname)

