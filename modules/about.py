# -*- coding: utf-8 -*-

# About module.
import os
import subprocess
import time

from lib.module import PCL_Module

class AboutModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)

        # Dictionary with links, that PCL will insert in top bar
        self.navigation_top = {
            "link1": {
                "action"    : "about",
                "address"   : "/about/",
                "name"      : "About",
                "target"    : "_self",
                "position"  : 99
            }
        }
        self.git_modified = False

    def execute(self):
        # Read about data
        about_data = self.read_file(os.path.join(self.temp_config["PCL_PATH"], "l10n", self.language, "about"))
        self.get_git_data()

        data = {
            "action"                : "about",
            "title"                 : self.config["main"]["site_name"] + " - About",
            "page_data_here"        : True,
            "git_rev_id"            : self.git_rev_id,
            "git_rev_count"         : self.git_rev_count,
            "git_last_commit_date"  : self.git_last_commit_date,
            "git_modified"          : self.git_modified,
            "page_data"             : about_data
        }
        self.renderer.print_output(data, template = "about.pyhtml")

    def get_git_data(self):
        # Gathering revisions count.
        proc = subprocess.Popen(["git", "rev-list", "--count", "HEAD"], stdout=subprocess.PIPE)
        self.git_rev_count = proc.stdout.read()

        # Gathering last revision data.
        proc = subprocess.Popen(["git", "rev-parse", "--verify", "HEAD"], stdout=subprocess.PIPE)
        rev_data = proc.stdout.read()

        # Format last revision data.
        self.git_rev_id_long = rev_data
        self.git_rev_id = rev_data[:8]

        # Get commit date.
        self.git_last_commit_date = time.strftime("%d %B %Y @ %H:%S", time.localtime(os.path.getmtime(os.path.join(self.temp_config["PCL_PATH"], ".git", "index"))))

        # Get modified flag
        proc = subprocess.Popen(["git", "ls-files", "-m"], stdout=subprocess.PIPE)
        data = data = proc.stdout.read().decode().split("\n")
        if len(data) > 1:
            self.git_modified = True

