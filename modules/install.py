# -*- coding: utf-8 -*-

# Install launcher module.
# Launching installation if PCL wasn't installed,
# otherwise prints error message and block any
# possible actions.
import os

from lib.module import PCL_Module

class InstallModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)
        self.auth_required = False

    def execute(self):
        """
        Executes on request.
        """
        # Check for install lock file.
        if not os.path.exists(os.path.join(self.temp_config["PCL_PATH"], "data", "install.lock")):
            self.proceed()
        else:
            data = {
                "action"        : "install",
                "site_name"     : self.config["main"]["site_name"],
                "error_header"  : "Already installed",
                "error_name"    : "PCLAlreadyInstalledError",
                "error_message" : "<p>PCL was already installed.</p> \
                                    <p>If you think that this is a mistake - remove \
                                    <span style='color: #66ff66'>install.lock</span> \
                                    file from <span style='color: #66ff66'>install</span> \
                                    directory."
            }
            self.renderer.print_output(data, template = "generic_error.pyhtml")

    def proceed(self):
        steps = {
            "1" : self.step_one,
            "2" : self.step_two,
            "3" : self.step_three
        }
        # Lets figure out what we launched.
        if not "step" in self.parameters[0]:
            self.step_one()
        else:
            steps[self.parameters[0]["step"][0]]()

    def step_one(self):
        """
        Step one - print some information.
        """
        data = {
            "root"              : "/install/",
            "hide_navbar_links" : True,
            "site_name"         : "PCL Installation - Step 1",
            "step"              : "1",
            "next_step"         : "2"
        }
        self.renderer.print_output(data, template = "install.pyhtml")

    def step_two(self):
        """
        Step two - asks for database credentials.
        """
        data = {
            "root"              : "/install/",
            "hide_navbar_links" : True,
            "site_name"         : "PCL Installation - Step 2",
            "step"              : "2",
            "next_step"         : "3",
        }
        self.renderer.print_output(data, template = "install.pyhtml")

    def step_three(self):
        """
        Step three - asks for administrator credentials.
        """
        data = {
            "root"              : "/install/",
            "hide_navbar_links" : True,
            "site_name"         : "PCL Installation - Step 3",
            "step"              : "3",
            "next_step"         : "4",
            "data"              : "<p>Step 3 placeholder</p>"
        }
        self.renderer.print_output(data, template = "install.pyhtml")