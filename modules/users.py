# -*- coding: utf-8 -*-

# Users actions module
import hashlib
from time import strftime, localtime

from lib.module import PCL_Module
from lib import user

class UsersModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)
        user.User.__init__(self)
        
        self.navigation_top = {
            "link1": {
                "action"    : "users",
                "address"   : "/users/",
                "name"      : "Users",
                "target"    : "_self",
                "position"  : 70
            }
        }

    def execute(self):
        mode = self.parameters[0]["id"]

        if not mode or mode == "list":
            self.show_users_list()
        else:
            self.show_user_data(mode)


    def show_users_list(self):
        """
        Shows users list.
        """
        users_list = []
        # Get users data and format it!
        users_data = self.database.get_all_users()
        for user in users_data:
            user_string = str(user[0]) + "###" + user[1] + "###" + str(user[3]) + "###" + strftime("%d %B %Y @ %H:%M", localtime(user[6])) + "###" + str(user[9]) + "###" + self.get_avatar(user[2])
            users_list.append(user_string)

        data = {
            "template_action"        : "list",
            "users"         : users_list
        }

        self.renderer.print_output(data, template = "user.pyhtml")

    def show_user_data(self, user_id):
        """
        Shows user profile for specified user.
        """
        user_info = []
        user_data = self.database.get_specified_user(user_id)
        for index, item in enumerate(user_data):
            if index == 3:
                user_info.append(strftime("%d %B %Y @ %H:%M", localtime(item)))
            else:
                user_info.append(item)

        data = {
            "template_action"        : "user",
            "user_info"         : user_info,
            "avatar"            : self.get_avatar(user_info[2])
        }
        self.renderer.print_output(data, template = "user.pyhtml")

    def get_avatar(self, email):
        """
        Returns gravatar link to avatar.
        """
        return "http://gravatar.com/avatar/" + hashlib.md5(email.encode()).hexdigest()