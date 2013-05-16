# -*- coding: utf-8 -*-

# Registrations module.

import os
import cgi
import hashlib
import random
import string

from lib.module import PCL_Module
from lib import mailer

class RegisterModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)

        self.rand_items = string.digits + string.ascii_uppercase

    def execute(self):
        # Read the rules!
        self.rules = self.read_file(os.path.join(self.temp_config["PCL_PATH"], "l10n", self.language, "rules"))
        self.proceed()

    def proceed(self):
        """
        Determine current step and execute approriate method.
        """
        steps = {
            "1" : self.step_one,
            "2" : self.step_two,
            "3" : self.step_three
        }

        # Lets figure out what we launched.
        if self.parameters[0]["id"] == "" or self.parameters[0]["id"] == None:
            self.step_one()
        else:
            steps[self.parameters[0]["id"]]()

    def step_one(self):
        """
        Step one - rules.
        """
        data = {
            "action"    : "register",
            "title"     : self.config["main"]["site_name"] + " - Registration, step 1",
            "rules"     : self.rules,
            "step"      : "1",
            "next_step" : "2",
            "submit"    : False
        }
        self.renderer.print_output(data, template = "register.pyhtml")

    def step_two(self):
        """
        Step two - user data.
        """
        data = {
            "action"    : "register",
            "title"     : self.config["main"]["site_name"] + " - Registration, step 2",
            "step"      : "2",
            "next_step" : "3",
            "submit"    : True,
            "error"     : False
        }
        self.renderer.print_output(data, template = "register.pyhtml")

    def step_three(self):
        """
        Step three - activation notification.
        """
        FAIL_DETECTED = False
        USERNAME_EXISTS = False
        PW_NOT_MATCH = False
        EMAIL_NOT_MATCH = False
        # Get form data
        username_raw = self.get_field_value("username")
        username_exists = self.database.get_userid_by_login(username_raw)
        if username_exists == "USERNAME_NOT_EXIST":
            username = username_raw
        else:
            FAIL_DETECTED = True
            USERNAME_EXISTS = True

        pw_raw = self.get_field_value("password")
        pw_raw_repeated = self.get_field_value("passwordRepeat")
        if pw_raw == pw_raw_repeated:
            password = hashlib.md5(pw_raw.encode()).hexdigest()
        else:
            FAIL_DETECTED = True
            PW_NOT_MATCH = True

        email_raw = self.get_field_value("email")
        email_raw_repeated = self.get_field_value("emailRepeat")
        if email_raw == email_raw_repeated:
            email = email_raw
        else:
            FAIL_DETECTED = True
            EMAIL_NOT_MATCH = True

        if FAIL_DETECTED:
            data = {
            "action"    : "register",
            "title"     : self.config["main"]["site_name"] + " - Registration, step 2",
            "step"      : "2",
            "next_step" : "3",
            "submit"    : True,
            "error"     : []
            }
            if USERNAME_EXISTS:
                data["error"].append("Username already exists.")
            if PW_NOT_MATCH:
                data["error"].append("Passwords you entered didn't match.")
            if EMAIL_NOT_MATCH:
                data["error"].append("E-Mails you entered didn't match.")

            self.renderer.print_output(data, template = "register.pyhtml")
        else:
            data = {
                "action"    : "register",
                "title"     : self.config["main"]["site_name"] + " - Registration, step 3",
                "step"      : "3",
                "next_step" : "4",
                "entered"   : cgi.FieldStorage(),
                "submit"    : False,
                "username"  : username
            }

            # Write to database.
            user_id = self.database.add_user(username, password, email)
            if user_id == "USER_EXISTS":
                data = {
                    "site_name"     : self.config["main"]["site_name"] + " - We got an error!",
                    "template_name" : "",
                    "error_header"  : "User already present",
                    "error_name"    : "UserAlreadyPresentError",
                    "error_message" : "Username you're trying to register already \
                                    present in database."
                }
                self.renderer.print_output(data, template = "generic_error.pyhtml")
            else:
                # Generate random string for activation.
                activation_string = ""
                for iteration in range(0, 25):
                    activation_string += random.choice(self.rand_items)

                self.database.add_activation(user_id, activation_string)
        
                activation_data = {
                    "site_address"      : self.config["main"]["site_address"],
                    "site_name"         : self.config["main"]["site_name"],
                    "username"          : username,
                    "activation_hash"   : activation_string
                }
                activation_mail = self.read_file(os.path.join(self.temp_config["PCL_PATH"], "l10n", self.language, "activation_mail"))
                activation_mail = activation_mail.format(**activation_data)
                mail = mailer.Mailer()
                mail.process_mail(email, "Activation on {0}".format(self.config["main"]["site_name"]), activation_mail)

                self.renderer.print_output(data, template = "register.pyhtml")