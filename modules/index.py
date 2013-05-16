# -*- coding: utf-8 -*-

# Index page module.

from lib.module import PCL_Module

class IndexModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)

        self.navigation_top = {
            "link1" : {
                "action"    : "home",
                "address"   : "/",
                "name"      : "Home",
                "target"    : "_self",
                "position"  : 0
            }
        }

    def execute(self):
        data = {}
        self.renderer.print_output(data)