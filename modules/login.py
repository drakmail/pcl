# -*- coding: utf-8 -*-

# Login module.
import datetime
import hashlib
import os

from lib.module import PCL_Module

class LoginModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)
        self.auth_required = False

    def execute(self):
        if self.parameters[0]["id"] == "" or not self.parameters[0]["id"]:
            self.show_login_form()
        elif self.parameters[0]["id"] == "out":
            self.log_out()
        else:
            self.check_and_generate_session()

    def show_login_form(self):
        """
        Shows login form and nothing more.
        """
        data = {
            "action"                : "login",
            "state"                 : "beginning",
            "title"                 : self.config["main"]["site_name"] + " - Log In",
            "credentials_status"    : "Enter your credentials."
        }

        self.renderer.print_output(data, template = "login.pyhtml")

    def check_and_generate_session(self):
        """
        Checking supplied credentials. If credentials is ok - place
        a cookie with unique hash.
        """
        username = self.get_field_value("username")
        password = self.database.get_password(username)
        activated = self.database.get_activation_status(username)

        if hashlib.md5(self.get_field_value("password").encode()).hexdigest() == password:
            if activated:
                # WOOHOO! User provided correct username/password combination!
                # Let's do something really useful with it. For example,
                # generate session cookie. But first we need to get
                # user's IP and browser string.
                user_ip = self.parameters[1]
                user_agent = os.environ["HTTP_USER_AGENT"]
                # Expiration timeout for cookie.
                expiration_timeout = datetime.datetime.now() + datetime.timedelta(days=30)
                expiration_timeout = [expiration_timeout.strftime("%s"), expiration_timeout.strftime("%A, %d-%b-%Y %H:%M:%S GMT")]
                # Transmit gathered data to cookies generator.
                session_string = self.session.generate_session(username, password, user_ip, user_agent, expiration_timeout[0])
                # Put this session string to database. But first get user ID.
                user_id = self.database.get_userid_by_login(username)
                # Put it! PUT IT!
                self.database.put_session_for_user_id(user_id, session_string, user_ip, user_agent, expiration_timeout[0])
                cookie = self.session.put_session_in_cookie(user_id, session_string, expiration_timeout[1])
                data = {
                    "action"                : "login",
                    "state"                 : "success",
                    "credentials_status"    : "Success!",
                    "cookie"                : cookie
                }
            else:
                data = {
                    "action"                : "login",
                    "state"                 : "fail",
                    "title"                 : self.config["main"]["site_name"] + " - Log In",
                    "credentials_status"    : "<span style='color: #ff9999;'>This user is not activated Check your mail for activation link.</span>"
                }
        else:
            data = {
                "action"                : "login",
                "state"                 : "fail",
                "title"                 : self.config["main"]["site_name"] + " - Log In",
                "credentials_status"    : "<span style='color: #ff9999;'>Username and password combination incorrect.</span>"
            }

        self.renderer.print_output(data, template = "login.pyhtml")

    def log_out(self):
        """
        Log user out. Nuff said.
        """
        # Generate fake cookies.
        user_id = self.session.get_cookie()["name"].value
        session_string = self.session.get_cookie()["hash"].value
        expiration_timeout = datetime.datetime.fromtimestamp(0)
        expiration_timeout =  expiration_timeout.strftime("%A, %d-%b-%Y %H:%M:%S GMT")
        cookie = self.session.put_session_in_cookie(user_id, session_string, expiration_timeout)
        data = {
            "action"                : "logout",
            "state"                 : "success",
            "title"                 : self.config["main"]["site_name"] + " - Log Out",
            "credentials_status"    : "",
            "cookie"                : cookie
        }
        self.session.remove_session_by_user_id(user_id)
        self.renderer.print_output(data, template = "login.pyhtml")

