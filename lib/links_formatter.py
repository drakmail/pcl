# -*- coding: utf-8 -*-

# Navigation links formatter.
# Format navigation links in approriate format and manner.
# Includes active and not active links classes.
import os
import sys
import inspect

from lib import common

class Links_Formatter:
    def __init__(self):
        self.links = {}
        self.formatted_links = [None] * 100

        # Make this class to be accessible thru "common" module.
        common.set_linksformatter(self)

        # Import all modules and get links from them.
        modules_list = os.listdir(os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "modules"))
        for item in modules_list:
            if item in ("__pycache__", "__init__.py"):
                # Ignore them
                continue

            module_name = item[:-3]
            # Let's try to load it!
            try:
                __import__("modules." + module_name)
            except ImportError as e:
                pass

            module = sys.modules["modules." + module_name]
            exec("self.module_instance = module." + module_name.capitalize() + "Module()")
            #if self.module_instance
            for module_member in inspect.getmembers(self.module_instance):
                if module_member[0] == "navigation_top":
                    self.links[module_name] = self.module_instance.navigation_top

    def get_links(self, action):
        """
        Returns formatted links list.
        """
        for key in self.links:
            for subkey in self.links[key]:
                if action == self.links[key][subkey]["action"].lower():
                    link = "<li class='active'><a href='{address}' target='{target}'>{name}</a></li>".format(**self.links[key][subkey])
                else:
                    link = "<li><a href='{address}' target='{target}'>{name}</a></li>".format(**self.links[key][subkey])
                self.formatted_links.insert(self.links[key][subkey]["position"], link)

        for index, item in enumerate(self.formatted_links):
            if item == "None":
                self.formatted_links.pop(index)

        return self.formatted_links
