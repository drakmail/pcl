# -*- coding: utf-8 -*-

# Health module.
# Just some system information.
import os
import platform
import pymysql

from lib.module import PCL_Module
from tenjin import tenjin

class HealthModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)
        self.auth_required = False

        self.navigation_top = {
            "link1": {
                "action"    : "health",
                "address"   : "/health/",
                "name"      : "System health",
                "target"    : "_self",
                "position"  : 80
            }
        }

    def execute(self):
        """
        Show some system info
        """
        # Gathering some useful info.
        data = {
            "action"                : "health",
            "resolution"            : "All systems is OK",
            "health_data_system"    : [
                "Python interpreter version###" + platform.python_version(),
                "PyMySQL version###" + pymysql.__version__,
                "Tenjin version###" + tenjin.__version__
            ]

        }

        self.renderer.print_output(data, template = "health.pyhtml")