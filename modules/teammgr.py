# -*- coding: utf-8 -*-

# Team management module
import os

from lib.module import PCL_Module

class TeammgrModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)
        self.set_temp_setting("AUTH_REQUIRED", True)

    def execute(self):
        actions = {
            "create"    : self.create_team,
            "rules"     : self.show_rules
        }
        if not self.parameters[0]["id"]:
            self.main_page()
        else:
            actions[self.parameters[0]["id"]]()

    def main_page(self):
        """
        """
        data = {
            "team_action"   : "index",
            "primary_team"  : "No team",
            "teams"         : ["Team 1###/teammgr/show/1/###player", "Team 2###/teammgr/show/2/###admin"],
        }

        self.renderer.print_output(data, template = "team_manage.pyhtml")

    def create_team(self):
        """
        """
        rules = self.read_file(os.path.join(self.temp_config["PCL_PATH"], "l10n", self.language, "team_creation_rules"))
        data = {
            "team_action"   : "create",
            "primary_team"  : "No team",
            "teams"         : ["Team 1###/show/1/###player", "Team 2###/show/2/###admin"],
            "rules"         : rules
        }

        self.renderer.print_output(data, template = "team_manage.pyhtml")

    def show_rules(self):
        """
        Show team creation rules.
        """
        rules = self.read_file(os.path.join(self.temp_config["PCL_PATH"], "l10n", self.language, "team_creation_rules"))
        data = {
            "team_action"   : "rules",
            "primary_team"  : "No team",
            "teams"         : ["Team 1###/show/1/###player", "Team 2###/show/2/###admin"],
            "rules"         : rules
        }

        self.renderer.print_output(data, template = "team_manage.pyhtml")

