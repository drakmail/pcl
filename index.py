#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL Index file.

import os
import sys

# Adding os.getcwd() (aka webserver root) into sys.path for
# any possible modules we might require.
if not os.path.join(os.getcwd(), "thirdparty") in sys.path:
    sys.path.insert(0, os.path.join(os.getcwd(), "thirdparty"))

from lib import common
# Set path for this script.
path = os.sep.join(sys.modules["lib.common"].__file__.split(os.sep)[:-2])
common.set_pcl_path(path)

from lib import config
from lib import links_formatter
from lib import web

class PCL:
    """
    Hello, this is PCL. It's not completed yet. Have fun :P
    """
    def __init__(self):
        #sys.stdout.buffer.write(b"Content-type: text/html; charset=utf8\n\n")
        # Set config
        self.config = config.Configuration().get_config()
        common.set_settings_dict(self.config)
        # PCL Version
        pcl_version = open(os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "version")).read()
        common.set_version(pcl_version)
        # Links formatter instance.
        self.links_formatter = links_formatter.Links_Formatter()
        # Renderer instance for parameters parsing.
        # TODO: make parse_parameters() a separate thing.
        self.renderer = web.Web()
        self.parameters = common.parse_parameters()
        #sys.stdout.buffer.write(str(self.parameters[0]).encode())
        
        if self.parameters[0].get("module") == "" or self.parameters[0].get("module") == None:
            # Load index page, as "module" is empty
            from modules import index
            index = index.IndexModule()
            index.execute()
        else:
            module_name = self.parameters[0].get("module")
            # Figuring out what module we need.
            modules_list = os.listdir(os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "modules"))
            if module_name + ".py" in modules_list:
                # Let's try to load it!
                try:
                    __import__("modules." + module_name)
                except ImportError as e:
                    pass

                module = sys.modules["modules." + module_name]
                # Execute module main class.
                exec("self.module_instance = module." + module_name.capitalize() + "Module()")
                self.module_instance.execute()
            else:
                # Ops... Module not found! Print an error message!
                data = {
                    "site_name"     : self.config["main"]["site_name"],
                    "error_header"  : "Module not found",
                    "error_name"    : "ModuleNotFoundError",
                    "error_message" : "<p>PCL can't find module <span style='color: #66ff66'>{0}</span>.</p>".format(module_name)
                }
                self.renderer.print_output(data, template = "generic_error.pyhtml")
            #else:
            #    data = {
            #        "site_name"     : self.config["main"]["site_name"],
            #        "error_header"  : "Bad parameters",
            #        "error_name"    : "BadParametersError",
            #        "error_message" : "<p>Parameters you provided are invalid.</p>"
            #    }
            #    self.renderer.print_output(data, template = "generic_error.pyhtml")
    def get_response(self):
        """
        (u)WSGI handler.
        """
        return common.HTML_RESPONSE
        
if __name__ == "__main__":
    PCL()