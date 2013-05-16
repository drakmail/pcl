# -*- coding: utf-8 -*-

# Dashboard module.

from lib.module import PCL_Module

class DashboardModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)
        self.set_temp_setting("AUTH_REQUIRED", True)

    def execute(self):
        """
        """
        # No actions here, passing directly.
        self.index()

    def index(self):
        """
        Dashboard index page.
        """
        data = {}
        self.renderer.print_output(data, template = "dashboard.pyhtml")